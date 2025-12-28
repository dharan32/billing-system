import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from fastapi import BackgroundTasks
from dotenv import load_dotenv

load_dotenv()


def send_invoice_email(
    background_tasks: BackgroundTasks,
    to_email: str,
    subject: str,
    bill: dict
):
    """Send invoice email asynchronously using SMTP."""
    background_tasks.add_task(
        _send_email,
        to_email,
        subject,
        bill
    )


def _send_email(to_email: str, subject: str, bill: dict):
    """Compose and send HTML invoice email."""

    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER", "dharan32d@gmail.com")
    smtp_password = os.getenv("SMTP_PASSWORD", "uldz dqnf epsl cglo")

    if not smtp_user or not smtp_password:
        print("SMTP config missing. Email not sent.")
        return

    items_html = ""
    for item in bill["items"]:
        items_html += f"""
        <tr>
            <td>{item['product_id']}</td>
            <td>{item['quantity']}</td>
            <td>{item['unit_price']}</td>
            <td>{item['tax_percentage']}%</td>
            <td>{item['subtotal']}</td>
        </tr>
        """

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h2>Invoice</h2>

        <p><strong>Customer Email:</strong> {bill['customer_email']}</p>

        <table border="1" cellpadding="8" cellspacing="0" width="100%">
            <tr style="background-color:#f2f2f2;">
                <th>Product ID</th>
                <th>Quantity</th>
                <th>Unit Price</th>
                <th>Tax (%)</th>
                <th>Subtotal</th>
            </tr>
            {items_html}
        </table>

        <br>

        <p><strong>Total Amount:</strong> {bill['total_amount']}</p>
        <p><strong>Paid Amount:</strong> {bill['paid_amount']}</p>
        <p><strong>Balance Amount:</strong> {bill['balance_amount']}</p>

        <br>
        <p>Thank you for shopping with us!</p>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        print(f"Invoice email sent successfully to {to_email}")
    except Exception as e:
        print(f"Email sending failed: {e}")
