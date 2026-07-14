/**
 * Soul Fuel Juice — Orders webhook (Google Apps Script)
 *
 * SETUP (one time):
 *  1. Open the "Soul Fuel Juice — Orders" Google Sheet.
 *  2. Extensions → Apps Script. Delete any sample code and paste ALL of this.
 *  3. Click Save. Then run setupSheet() once (top toolbar ▶) to apply the
 *     brand colors — approve the permission prompt when asked.
 *  4. Deploy → New deployment → gear icon → "Web app".
 *       Description: Orders webhook
 *       Execute as: Me
 *       Who has access: Anyone
 *     → Deploy → authorize → COPY the "Web app URL" (ends in /exec).
 *  5. Send that URL to Claude — it gets pasted into js/square-config.js
 *     (window.SHEETS_WEBHOOK) so every order is logged to this sheet.
 */

var HEADERS = ['Date', 'Order #', 'Name', 'Phone', 'Email', 'Fulfillment',
               'Address', 'Items', 'Total', 'Payment', 'Notes'];

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(30000);
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
    ensureHeader_(sheet);
    var d = {};
    try { d = JSON.parse(e.postData.contents); } catch (_) {}
    sheet.appendRow([
      new Date(), d.order || '', d.name || '', d.phone || '', d.email || '',
      d.fulfillment || '', d.address || '', d.items || '', d.total || '',
      d.payment || '', d.notes || ''
    ]);
    return json_({ ok: true });
  } catch (err) {
    return json_({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}

function doGet() {
  return json_({ ok: true, message: 'Soul Fuel Juice orders webhook is live.' });
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function ensureHeader_(sheet) {
  if (sheet.getRange(1, 1).getValue() !== 'Date') {
    sheet.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]);
  }
  // Soul Fuel Juice branding: deep green header, cream text, gold tab.
  sheet.getRange(1, 1, 1, HEADERS.length)
    .setBackground('#1C3527').setFontColor('#FAF6ED').setFontWeight('bold');
  sheet.setFrozenRows(1);
  try { sheet.setTabColor('#C6A15B'); } catch (_) {}
  for (var c = 1; c <= HEADERS.length; c++) { sheet.autoResizeColumn(c); }
}

// Run once from the editor to brand the sheet immediately.
function setupSheet() {
  ensureHeader_(SpreadsheetApp.getActiveSpreadsheet().getSheets()[0]);
}
