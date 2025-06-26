PoultryDetect+ : AI-Based Poultry Disease Detection and Report Generator
=======================================================================

Project Description:
--------------------
PoultryDetect+ is a web-based AI application designed to assist poultry farm owners, veterinary students, and researchers in identifying poultry diseases from images, providing suggested medicines, symptoms, and generating downloadable reports. The application also offers a training and research hub with veterinary guidelines and AI resources.

Features:
---------
✔ Upload images to predict poultry diseases  
✔ Display prediction percentage and related symptoms  
✔ Suggest appropriate medicines for identified conditions  
✔ Download diagnosis reports as PDF  
✔ Access veterinary research case studies and guidelines  
✔ AI training tutorials for students  
✔ Consistent modern UI using Tailwind CSS  
✔ Logo and images for visual branding  
✔ Copyright footer on every page

Project Structure:
------------------
/static/                 -> Images, logos, CSS files  
/templates/              -> HTML template files (index.html, result.html, about.html, etc.)  
app.py                   -> Main Flask application  
/venv/                    -> Virtual environment (if used)  
requirements.txt         -> Python dependency list  
README.txt               -> Project description file (this file)

How to Run:
-----------
1. Install required packages:
   pip install -r requirements.txt

2. Run the Flask app:
   python app.py

3. Open the browser and visit:
   http://127.0.0.1:5000/

Assets Used:
------------
- PoultryDetect+ logo (static/logo.png)
- Poultry images for footer (static/hen1.jpeg, hen2.jpeg, hen3.jpeg, hen4.jpeg)
- Tailwind CSS CDN for UI styling
- Flask for backend routing and prediction display
- AI model (ensure model file and predict function available in app.py)

Author:
-------
Developed by Gowtham Raj 
Year: 2025  
Purpose: Veterinary research and practical AI application for poultry farming

Notes:
------
- Ensure all image files are placed inside the 'static' folder.
- The AI model should be loaded and integrated within 'app.py'.
- Update URLs in HTML templates if deploying online.
- Keep consistent image naming and file formats as referenced in HTML.

License:
--------
This project is for educational and research use. Commercial distribution is not permitted without permission.