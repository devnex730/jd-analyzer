from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
import json, re
from .keywords import extract_keywords


skills_db = [
    "Python", "JavaScript", "Java", "C Programming", "C++ Programming", "C#", "R Programming",
    "HTML", "CSS", "React.js", "Node.js", "Django", "FastAPI", "jQuery", "MERN",
    "Hibernate ORM(Java)", "J2EE", "JSP", "Spring MVC",
    "SQL", "MySQL", "PostgreSQL", "MongoDB",
    "Git", "GitHub", "Docker", "Linux",
    "AWS", "Azure", "GCP",
    "Machine Learning", "Data Analysis", "Pandas", "Numpy", "Scikit-Learn",
    "Power BI", "Tableau", "LangChain", "LLMOps", "TensorFlow", "PyTorch",
    "Natural Language Processing (NLP)", "Neural Networks",
    "Cybersecurity Basics", "Cybersecurity", "Cloud Computing",
    "Mobile App Development", "Flutter", "React Native",
    "UI/UX Designing", "UI & UX Design", "Figma", "Adobe XD",
    "Graphic Designing", "Visual Design", "Design Thinking", "Prototyping",
    "Digital Marketing", "Email Marketing", "Search Engine Optimization", "SEO",
    "Facebook Marketing", "Instagram Marketing", "Open Source",
    "Google Suite", "G Suite", "MS-Office", "Excel", "Data Science",
    "IoT (Esp32 / Arduino)", "PCB Designing", "Embedded Systems", "STM32",
    "ARM Microcontroller", "Sensors & Actuators", "Circuit Designing",
    "Robot Operating System (ROS)", "Robotics",
    "3D Modeling", "Blender 3D", "Animation", "Video Editing", "Video Making",
    "Adobe Creative Suite", "Adobe Photoshop", "Adobe Illustrator",
    "Adobe InDesign", "Adobe Premiere Pro", "Canva", "CorelDRAW", "CAD Drafting",
    "Creative Writing", "English Proficiency (Spoken)", "Critical Thinking",
    "Software Testing", "Unity Engine",
]

education_db = [
    "Bachelor", "Master", "B.Tech", "M.Tech", "Ph.D", "MBA",
    "B.Sc", "M.Sc", "BCA", "MCA", "Diploma", "Doctorate",
    "High School", "Graduate", "Postgraduate"
    ]

soft_skills_db = [
        "communication",
        "teamwork",
        "problem-solving",
        "adaptability",
        "leadership",
        "attention to detail"
    ]
                
# ---------------- PAGES ----------------
@csrf_exempt
def index(request):
    return render(request, "api/index.html")


@csrf_exempt
def resume(request):
    return render(request, "api/resume.html")

def extract_education(jd_text):
    degrees = sorted(dg for dg in education_db if dg.lower() in jd_text)
    return degrees

@csrf_exempt
def get_jd(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    data = json.loads(request.body or "{}")
    jd_x = data.get("jd")
    jd = jd_x.lower()

    if not jd:
        return JsonResponse({"error": "JD text missing"}, status=400)

    required_skills = sorted({skill for skill in skills_db if skill.lower() in jd})

    exp_match = re.findall(r'(\d+)\s*(?:[-to]+\s*(\d+))?\s*(?:years|year)', jd.lower())
    required_experience = ""
    if exp_match:
        years = []

        for start, end in exp_match:
            years.append(int(start))
            if end:
                years.append(int(end))

        required_experience = f"Minimum {min(years)} year(s) experience required."

    elif "fresher" in jd or "freshers" in jd:
        required_experience = "Freshers are allowed."
    else:
        required_experience = "Experience not specified."
        
    soft_skills = [s.title() for s in soft_skills_db if s in jd]

    important_keywords = extract_keywords(
        required_skills=required_skills,
        soft_skills=soft_skills, 
        jd_text=jd_x,
        )

    required_education = extract_education(jd_x)
    
    return JsonResponse({
        "required_skills": required_skills,
        "important_keywords": important_keywords,
        "required_experience": required_experience,
        "required_education": required_education,
    })
    

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def build_resume(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    full_name = request.POST.get("full_name")
    email = request.POST.get("email")
    phone = request.POST.get("phone")
    location = request.POST.get("location")
    summary = request.POST.get("summary")

    skills_raw = request.POST.get("skills", "")
    skills = [s.strip() for s in skills_raw.split(",") if s.strip()]

    job_titles = request.POST.getlist("job_title[]")
    companies = request.POST.getlist("company[]")
    descriptions = request.POST.getlist("experience_desc[]")

    experience = []
    for jt, comp, desc in zip(job_titles, companies, descriptions):
        if jt or comp or desc:
            experience.append({
                "job_title": jt,
                "company": comp,
                "description": desc,
            })

    degree = request.POST.get("degree")
    college = request.POST.get("college")
    year = request.POST.get("year")

    projects_raw = request.POST.get("projects", "")
    projects = [p.strip() for p in projects_raw.split("\n") if p.strip()]

    resume_data = {
        "personal": {
            "name": full_name,
            "email": email,
            "phone": phone,
            "location": location,
        },
        "summary": summary,
        "skills": skills,
        "experience": experience,
        "education": {
            "degree": degree,
            "college": college,
            "year": year,
        },
        "projects": projects,
    }

    request.session["resume_data"] = resume_data

    return JsonResponse({
        "status": "success",
        "redirect_url": "/resume/preview/"
    })


def resume_preview(request):
    resume_data = request.session.get("resume_data")
    if not resume_data:
        return redirect("build_resume/") 
    return render(request, "api/ans_resume.html", {"resume" : resume_data, "preview": True})

