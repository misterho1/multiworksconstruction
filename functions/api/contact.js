/**
 * Cloudflare Pages Function for /api/contact
 *
 * Replaces the legacy `mailto:` form action that:
 *   - silently failed on iOS Safari and webmail-only users (~30% of mobile)
 *   - leaked the destination email address in plaintext to scrapers
 *   - bypassed client-side validation in most browsers
 *
 * Architecture:
 *   1. Honeypot field (`company`) — bots fill every field; real users leave it blank.
 *   2. Field validation — required fields, basic email shape.
 *   3. If `env.RESEND_API_KEY` is set, sends a real email via Resend.
 *      Otherwise logs the submission to Cloudflare logs (visible in dashboard).
 *   4. Returns JSON success/error so the client-side script can render a status.
 *
 * Environment variables (set in Cloudflare Pages -> Settings -> Environment):
 *   RESEND_API_KEY    Resend.com API key (free 100/day tier is enough for a marketing site).
 *   CONTACT_TO        Destination email address (defaults to build@multiworksconstruction.com).
 *   CONTACT_FROM      From address for the email (must be on a verified Resend domain).
 *
 * No env vars set? Form still submits successfully; review submissions via
 * `wrangler pages deployment tail` or the Cloudflare Logs UI.
 */

const CONTACT_DEFAULT_TO = 'build@multiworksconstruction.com';

function jsonResponse(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8' },
  });
}

function isProbablyEmail(s) {
  return typeof s === 'string' && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s);
}

function escapeHtml(s) {
  return String(s ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function renderEmail(data) {
  const rows = [
    ['Name', data.name],
    ['Phone', data.phone],
    ['Email', data.email],
    ['City', data.city || '(not given)'],
    ['Service', data.service || '(not selected)'],
    ['Budget', data.budget || '(not given)'],
    ['Message', data.message || '(blank)'],
  ];
  const html = rows
    .map(([k, v]) => `<tr><th align="left" style="padding:8px 12px;border-bottom:1px solid #ddd">${escapeHtml(k)}</th><td style="padding:8px 12px;border-bottom:1px solid #ddd">${escapeHtml(v).replace(/\n/g, '<br>')}</td></tr>`)
    .join('');
  return `<table style="font-family:system-ui,sans-serif;font-size:14px;border-collapse:collapse">${html}</table>`;
}

export async function onRequestPost({ request, env }) {
  let data;
  try {
    const formData = await request.formData();
    data = Object.fromEntries(formData.entries());
  } catch (e) {
    return jsonResponse({ ok: false, error: 'Unable to read form data.' }, 400);
  }

  // Honeypot: if the bot filled `company`, silently accept (don't tell them it's a trap).
  if (data.company && data.company.trim().length > 0) {
    return jsonResponse({ ok: true });
  }

  const errors = [];
  if (!data.name || data.name.trim().length < 1) errors.push('Name is required.');
  if (!data.phone || data.phone.trim().length < 7) errors.push('A valid phone is required.');
  if (!isProbablyEmail(data.email)) errors.push('A valid email is required.');
  if (errors.length) {
    return jsonResponse({ ok: false, error: errors.join(' ') }, 400);
  }

  // Build the email payload.
  const to = env.CONTACT_TO || CONTACT_DEFAULT_TO;
  const from = env.CONTACT_FROM || 'Multiworks Site <noreply@multiworksconstruction.com>';
  const subject = `New consultation request from ${data.name}`;

  // Log the submission so it's visible even if the email send fails.
  console.log('[contact] new submission', {
    name: data.name,
    email: data.email,
    phone: data.phone,
    service: data.service,
    budget: data.budget,
    city: data.city,
    userAgent: request.headers.get('user-agent'),
    cfRay: request.headers.get('cf-ray'),
  });

  if (!env.RESEND_API_KEY) {
    // No email service wired yet. The submission is logged; return success so the
    // client renders a confirmation. The user will see logged entries in Cloudflare
    // until they add a RESEND_API_KEY env var.
    return jsonResponse({ ok: true, queued: false });
  }

  // Send via Resend (https://resend.com/docs/api-reference/emails/send-email).
  try {
    const resendRes = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'authorization': `Bearer ${env.RESEND_API_KEY}`,
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        from,
        to: [to],
        reply_to: data.email,
        subject,
        html: renderEmail(data),
        text: Object.entries(data)
          .filter(([k]) => k !== 'company')
          .map(([k, v]) => `${k}: ${v}`)
          .join('\n'),
      }),
    });
    if (!resendRes.ok) {
      const body = await resendRes.text();
      console.error('[contact] resend error', resendRes.status, body);
      return jsonResponse({ ok: false, error: 'Email delivery failed; please call us or try again.' }, 502);
    }
    return jsonResponse({ ok: true, queued: true });
  } catch (err) {
    console.error('[contact] dispatch error', err);
    return jsonResponse({ ok: false, error: 'Email delivery failed; please call us or try again.' }, 502);
  }
}

// Reject other methods.
export function onRequest({ request }) {
  return new Response(`Method ${request.method} not allowed`, {
    status: 405,
    headers: { 'allow': 'POST' },
  });
}
