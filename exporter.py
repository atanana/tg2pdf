import markdown
from weasyprint import HTML, CSS


def export_markdown_to_pdf(markdown_text: str, output_path: str):
    """
    Export markdown text to a PDF file.
    """
    html_content = markdown.markdown(markdown_text)

    # Wrap HTML in basic structure
    full_html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <link rel="stylesheet" href="markdown.css">
    </head>
    <body>
    {html_content}
    </body>
    </html>
    """

    # Generate PDF
    HTML(string=full_html, base_url='.').write_pdf(output_path, stylesheets=[CSS("markdown.css")])