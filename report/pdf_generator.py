from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


class PDFGenerator:

    def create(self, report_text, output_path):

        doc = SimpleDocTemplate(output_path)

        styles = getSampleStyleSheet()

        story = []

        for line in report_text.split("\n"):

            story.append(
                Paragraph(line, styles["BodyText"])
            )

        doc.build(story)

        return output_path