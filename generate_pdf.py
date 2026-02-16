#!/usr/bin/env python3
"""
Generate comprehensive PDF documentation for Blink Camera Archiver
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os


def generate_documentation_pdf():
    """Generate the complete PDF documentation"""

    output_path = '/home/user/inablink/Blink_Camera_Archiver_Documentation.pdf'

    # Create PDF document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    # Container for the 'Flowable' objects
    elements = []

    # Define styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=32,
        textColor=colors.HexColor('#2E4057'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#048A81'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )

    chapter_style = ParagraphStyle(
        'ChapterTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#2E4057'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold',
        borderWidth=2,
        borderColor=colors.HexColor('#048A81'),
        borderPadding=6,
        backColor=colors.HexColor('#E8F4F8')
    )

    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#048A81'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        leading=14
    )

    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontSize=9,
        fontName='Courier',
        backColor=colors.HexColor('#F5F5F5'),
        borderWidth=1,
        borderColor=colors.HexColor('#CCCCCC'),
        borderPadding=8,
        spaceAfter=10,
        spaceBefore=10,
        leftIndent=20,
        rightIndent=20
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['BodyText'],
        fontSize=10,
        leftIndent=30,
        bulletIndent=15,
        spaceAfter=6,
        leading=14
    )

    # Title Page
    elements.append(Spacer(1, 2*inch))
    elements.append(Paragraph("Blink Camera Archiver", title_style))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("Automatic Video Backup Solution", subtitle_style))
    elements.append(Spacer(1, 1*inch))
    elements.append(Paragraph("Protect your security footage from tampering or deletion", body_style))
    elements.append(Spacer(1, 2*inch))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%B %Y')}", body_style))
    elements.append(PageBreak())

    # Table of Contents
    elements.append(Paragraph("Table of Contents", chapter_style))
    elements.append(Spacer(1, 0.2*inch))
    toc_items = [
        '1. Overview',
        '2. Features',
        '3. Requirements',
        '4. Installation',
        '5. Configuration',
        '6. Usage',
        '7. Running as a Service',
        '8. Code Structure',
        '9. Troubleshooting',
        '10. Security Notes',
        '11. API Information',
        '12. License and Credits'
    ]
    for item in toc_items:
        elements.append(Paragraph(f"• {item}", bullet_style))
    elements.append(PageBreak())

    # 1. Overview
    elements.append(Paragraph("1. Overview", chapter_style))
    elements.append(Paragraph(
        "The Blink Camera Archiver is a Python-based tool that automatically downloads and "
        "archives video clips from your Blink home security cameras. It runs at regular intervals "
        "and saves all new videos to local storage, protecting them from tampering or cloud deletion.",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "This tool is designed for users who want complete control over their security footage "
        "and want to ensure that videos are permanently backed up before they can be altered or "
        "removed from the cloud.",
        body_style
    ))
    elements.append(PageBreak())

    # 2. Features
    elements.append(Paragraph("2. Features", chapter_style))
    features = [
        'Automatic video archiving from all Blink cameras',
        'Tracks downloaded videos to avoid duplicates',
        'Organizes videos by camera name and date',
        'Respects Blink\'s API rate limits (60-second minimum)',
        'Supports 2FA authentication',
        'Configurable check intervals',
        'Can run as one-time check or continuous daemon',
        'Comprehensive logging and error handling',
        'Lightweight and efficient',
        'Cross-platform (Linux, macOS, Windows)',
        'Easy setup with automated scripts',
        'Can be configured as a system service'
    ]
    for feature in features:
        elements.append(Paragraph(f"• {feature}", bullet_style))
    elements.append(PageBreak())

    # 3. Requirements
    elements.append(Paragraph("3. Requirements", chapter_style))
    elements.append(Paragraph("System Requirements", section_style))
    requirements = [
        'Python 3.8 or later',
        'Internet connection',
        'Blink account with active cameras',
        'Sufficient storage space for video archives'
    ]
    for req in requirements:
        elements.append(Paragraph(f"• {req}", bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("Python Dependencies", section_style))
    dependencies = [
        'blinkpy >= 0.24.0 (Blink API library)',
        'aiohttp >= 3.9.0 (Async HTTP client)',
        'aiofiles >= 23.0.0 (Async file operations)',
        'python-dateutil >= 2.8.0 (Date parsing)'
    ]
    for dep in dependencies:
        elements.append(Paragraph(f"• {dep}", bullet_style))
    elements.append(PageBreak())

    # 4. Installation
    elements.append(Paragraph("4. Installation", chapter_style))
    elements.append(Paragraph("Quick Setup (Recommended)", section_style))
    elements.append(Paragraph("Run the automated setup script:", body_style))
    elements.append(Paragraph("<font face='Courier' size=9>chmod +x setup.sh<br/>./setup.sh</font>", code_style))
    elements.append(Paragraph("This will:", body_style))
    setup_steps = [
        'Create a Python virtual environment',
        'Install all required dependencies',
        'Create a config.json file from the example'
    ]
    for step in setup_steps:
        elements.append(Paragraph(f"• {step}", bullet_style))

    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("Manual Installation", section_style))
    elements.append(Paragraph("If you prefer manual setup:", body_style))
    manual_code = """# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and edit config
cp config.example.json config.json"""
    elements.append(Paragraph(f"<font face='Courier' size=9>{manual_code}</font>", code_style))
    elements.append(PageBreak())

    # 5. Configuration
    elements.append(Paragraph("5. Configuration", chapter_style))
    elements.append(Paragraph("Edit config.json with your Blink account credentials and preferences:", body_style))
    config_code = """{
  "username": "your_blink_email@example.com",
  "password": "your_blink_password",
  "download_path": "./videos",
  "check_interval_seconds": 300,
  "archive_db_path": "./archive_db.json",
  "log_file": "./blink_archiver.log",
  "log_level": "INFO"
}"""
    elements.append(Paragraph(f"<font face='Courier' size=9>{config_code}</font>", code_style))

    elements.append(Paragraph("Configuration Parameters", section_style))
    config_params = [
        '<b>username:</b> Your Blink account email address',
        '<b>password:</b> Your Blink account password',
        '<b>download_path:</b> Directory where videos will be saved',
        '<b>check_interval_seconds:</b> How often to check for new videos (min 60)',
        '<b>archive_db_path:</b> Path to database tracking downloaded videos',
        '<b>log_file:</b> Path to the log file',
        '<b>log_level:</b> Logging verbosity (DEBUG, INFO, WARNING, ERROR)'
    ]
    for param in config_params:
        elements.append(Paragraph(f"• {param}", bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("Two-Factor Authentication", section_style))
    elements.append(Paragraph(
        "If your Blink account has 2FA enabled, you will be prompted to enter the verification "
        "code when running the archiver. The code will be sent to your registered email or phone.",
        body_style
    ))
    elements.append(PageBreak())

    # 6. Usage
    elements.append(Paragraph("6. Usage", chapter_style))
    elements.append(Paragraph("Basic Usage", section_style))
    elements.append(Paragraph("Command syntax:", body_style))
    elements.append(Paragraph("<font face='Courier' size=9>python3 blink_archiver.py [OPTIONS]</font>", code_style))

    elements.append(Paragraph("Command-Line Options", section_style))
    options = [
        '<b>--config PATH:</b> Path to configuration file (default: config.json)',
        '<b>--once:</b> Run once and exit (default: run continuously)',
        '<b>--since-days N:</b> Download videos from the last N days (default: 1)'
    ]
    for opt in options:
        elements.append(Paragraph(f"• {opt}", bullet_style))

    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("Usage Examples", section_style))

    elements.append(Paragraph("Run once to test:", body_style))
    elements.append(Paragraph("<font face='Courier' size=9>./run.sh --once</font>", code_style))

    elements.append(Paragraph("Run continuously (default mode):", body_style))
    elements.append(Paragraph("<font face='Courier' size=9>./run.sh</font>", code_style))

    elements.append(Paragraph("Run in background:", body_style))
    elements.append(Paragraph("<font face='Courier' size=9>nohup ./run.sh &amp;</font>", code_style))

    elements.append(Paragraph("Download videos from the last 7 days:", body_style))
    elements.append(Paragraph("<font face='Courier' size=9>python3 blink_archiver.py --once --since-days 7</font>", code_style))
    elements.append(PageBreak())

    # 7. Running as a Service
    elements.append(Paragraph("7. Running as a Service", chapter_style))

    elements.append(Paragraph("systemd (Linux)", section_style))
    elements.append(Paragraph("Create a systemd service file:", body_style))
    elements.append(Paragraph("<font face='Courier' size=9>sudo nano /etc/systemd/system/blink-archiver.service</font>", code_style))

    systemd_code = """[Unit]
Description=Blink Camera Archiver
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/inablink
ExecStart=/path/to/inablink/run.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target"""
    elements.append(Paragraph(f"<font face='Courier' size=9>{systemd_code}</font>", code_style))

    elements.append(Paragraph("Enable and start the service:", body_style))
    systemd_commands = """sudo systemctl enable blink-archiver
sudo systemctl start blink-archiver
sudo systemctl status blink-archiver"""
    elements.append(Paragraph(f"<font face='Courier' size=9>{systemd_commands}</font>", code_style))

    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("cron (Linux/macOS)", section_style))
    elements.append(Paragraph("For periodic checks, add to crontab:", body_style))
    elements.append(Paragraph("<font face='Courier' size=9>crontab -e</font>", code_style))
    elements.append(Paragraph("Add this line (runs every 5 minutes):", body_style))
    elements.append(Paragraph("<font face='Courier' size=9>*/5 * * * * /path/to/inablink/run.sh --once &gt;&gt; /path/to/cron.log 2&gt;&amp;1</font>", code_style))
    elements.append(PageBreak())

    # 8. Code Structure
    elements.append(Paragraph("8. Code Structure", chapter_style))

    elements.append(Paragraph("Main Components", section_style))
    elements.append(Paragraph("BlinkArchiver Class:", body_style))
    components = [
        '<b>__init__:</b> Initialize archiver with configuration',
        '<b>authenticate:</b> Handle Blink authentication and 2FA',
        '<b>get_all_cameras:</b> Retrieve list of all cameras',
        '<b>download_new_videos:</b> Download videos not yet archived',
        '<b>run_once:</b> Execute single archival cycle',
        '<b>run_continuous:</b> Run continuous monitoring loop',
        '<b>cleanup:</b> Clean up resources on shutdown'
    ]
    for comp in components:
        elements.append(Paragraph(f"• {comp}", bullet_style))

    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("Directory Structure", section_style))
    dir_structure = """inablink/
├── blink_archiver.py       # Main script
├── config.json             # Your configuration
├── archive_db.json         # Downloaded videos database
├── blink_archiver.log      # Log file
├── videos/                 # Downloaded videos
│   ├── Front_Door/         # Camera folders
│   └── Backyard/
├── requirements.txt
├── setup.sh
└── README.md"""
    elements.append(Paragraph(f"<font face='Courier' size=9>{dir_structure}</font>", code_style))
    elements.append(PageBreak())

    # 9. Troubleshooting
    elements.append(Paragraph("9. Troubleshooting", chapter_style))

    elements.append(Paragraph("Authentication Fails", section_style))
    auth_solutions = [
        'Verify username and password in config.json',
        'Check if 2FA code was entered correctly',
        'Ensure account is not locked',
        'Try logging in through Blink app first',
        'Check internet connection'
    ]
    for solution in auth_solutions:
        elements.append(Paragraph(f"• {solution}", bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("No Videos Downloaded", section_style))
    no_video_solutions = [
        'Verify cameras have recorded videos',
        'Check videos exist in the Blink mobile app',
        'Try using --since-days flag with larger value',
        'Check log file for specific errors',
        'Ensure cameras are online and armed'
    ]
    for solution in no_video_solutions:
        elements.append(Paragraph(f"• {solution}", bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("Rate Limit Errors", section_style))
    rate_solutions = [
        'Ensure check_interval_seconds is at least 60',
        'Increase interval to 300 seconds (5 minutes) or more',
        'The Blink API recommends intervals of 60+ seconds',
        'Avoid running multiple instances simultaneously'
    ]
    for solution in rate_solutions:
        elements.append(Paragraph(f"• {solution}", bullet_style))
    elements.append(PageBreak())

    # 10. Security Notes
    elements.append(Paragraph("10. Security Notes", chapter_style))
    security_notes = [
        'Keep config.json secure - it contains your credentials',
        'Never commit config.json to version control',
        'The .gitignore file prevents committing sensitive files',
        'Consider using environment variables for credentials',
        'Regularly backup your archived videos to external storage',
        'Use strong, unique passwords for your Blink account',
        'Enable 2FA on your Blink account for extra security',
        'Set appropriate file permissions on config.json (chmod 600)',
        'Store archived videos on encrypted drives if possible',
        'Monitor log files for suspicious authentication attempts'
    ]
    for note in security_notes:
        elements.append(Paragraph(f"• {note}", bullet_style))
    elements.append(PageBreak())

    # 11. API Information
    elements.append(Paragraph("11. API Information", chapter_style))

    elements.append(Paragraph("Blink API Library", section_style))
    elements.append(Paragraph(
        "This tool uses the blinkpy library (github.com/fronzbot/blinkpy), which is actively "
        "maintained and provides a Python interface to the Blink camera API.",
        body_style
    ))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("Rate Limiting", section_style))
    elements.append(Paragraph("Important API guidelines:", body_style))
    rate_info = [
        'Minimum 60-second interval between API calls',
        'Default check interval is 300 seconds (5 minutes)',
        'Tool automatically enforces minimum intervals',
        'Excessive API calls can overwhelm Blink servers',
        'Tool implements delays between operations'
    ]
    for info in rate_info:
        elements.append(Paragraph(f"• {info}", bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("How It Works", section_style))
    workflow = [
        '1. Authenticates with Blink servers using credentials',
        '2. Retrieves list of all cameras on your account',
        '3. For each camera, fetches recent video clips',
        '4. Checks local database to avoid re-downloading',
        '5. Downloads new videos and saves organized by camera',
        '6. Updates tracking database with downloaded clip IDs',
        '7. Waits for configured interval and repeats'
    ]
    for step in workflow:
        elements.append(Paragraph(step, body_style))
    elements.append(PageBreak())

    # 12. License and Credits
    elements.append(Paragraph("12. License and Credits", chapter_style))

    elements.append(Paragraph("License", section_style))
    elements.append(Paragraph("This project is released under the MIT License.", body_style))
    elements.append(Paragraph(
        "Permission is hereby granted, free of charge, to any person obtaining a copy of this "
        "software and associated documentation files, to deal in the Software without restriction, "
        "including without limitation the rights to use, copy, modify, merge, publish, distribute, "
        "sublicense, and/or sell copies of the Software.",
        body_style
    ))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("Credits", section_style))
    elements.append(Paragraph("Built using the blinkpy library by fronzbot for Blink API access.", body_style))
    elements.append(Paragraph("GitHub: https://github.com/fronzbot/blinkpy", body_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("Disclaimer", section_style))
    elements.append(Paragraph(
        "This tool is not affiliated with or endorsed by Blink or Amazon. Use at your own risk. "
        "Ensure you comply with Blink's Terms of Service. The authors are not responsible for "
        "any issues that may arise from using this software.",
        body_style
    ))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("Contributing", section_style))
    elements.append(Paragraph(
        "Issues and pull requests are welcome at the project repository. "
        "Please follow standard GitHub contribution guidelines.",
        body_style
    ))
    elements.append(PageBreak())

    # Appendix
    elements.append(Paragraph("Appendix: Repository Information", chapter_style))

    elements.append(Paragraph("Git Repository", section_style))
    elements.append(Paragraph("<b>Repository:</b> stimutak/inablink", body_style))
    elements.append(Paragraph("<b>Branch:</b> claude/blink-camera-archiver-011CUUuc2imcDEExf48jUcWX", body_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("Files Committed", section_style))
    committed_files = [
        'blink_archiver.py (main script)',
        'requirements.txt',
        'config.example.json',
        'setup.sh',
        'run.sh',
        '.gitignore',
        'LICENSE',
        'README.md'
    ]
    for file in committed_files:
        elements.append(Paragraph(f"• {file}", bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("Pull Request", section_style))
    elements.append(Paragraph(
        "Create pull request at: https://github.com/stimutak/inablink/pull/new/claude/blink-camera-archiver-011CUUuc2imcDEExf48jUcWX",
        body_style
    ))

    # Build PDF
    doc.build(elements)
    print(f"PDF generated successfully: {output_path}")
    return output_path


if __name__ == '__main__':
    try:
        pdf_path = generate_documentation_pdf()
        print(f"\nPDF created: {pdf_path}")
    except Exception as e:
        print(f"Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
