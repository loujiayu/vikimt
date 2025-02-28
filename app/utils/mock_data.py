import json
import random
import logging
from datetime import datetime, timedelta

def get_mock_medical_response(is_soap=False, response_schema=None) -> str:
    """
    Generate mock medical AI responses for development/testing.
    
    Args:
        is_soap: Whether to generate SOAP notes format
        response_schema: Schema for structured responses
        
    Returns:
        str: Mock AI response
    """
    if is_soap:
        return get_mock_soap_notes()
    elif response_schema:
        return get_mock_structured_response(response_schema)
    else:
        return get_mock_general_response()
        
def get_mock_soap_notes() -> str:
    """Generate mock SOAP notes"""
    mock_soap_templates = [
        """
# SOAP Notes

## Subjective
Patient reports {symptom} for {duration}. {additional_complaint}. Patient describes the pain as {pain_description}. No reported fever or chills. {medication_statement}

## Objective
- BP: {bp_systolic}/{bp_diastolic} mmHg
- HR: {heart_rate} bpm
- RR: {resp_rate} breaths/min
- Temp: {temp}°F
- SpO2: {spo2}% on room air

Physical examination reveals {physical_finding}. {additional_finding}

## Assessment
1. {diagnosis} - {diagnosis_detail}
2. {secondary_condition} - Likely related to {relation_factor}

## Plan
1. {medication_plan}
2. {followup_plan}
3. {additional_recommendation}
4. Follow up in {followup_timing} to reassess.
        """,
        
        """
# Patient SOAP Documentation

### S (Subjective)
Patient is a {age}-year-old {gender} presenting with chief complaint of "{chief_complaint}" that started {onset_time}. {symptom_description}. Patient rates pain as {pain_level}/10. {history_element}.

### O (Objective)
Vitals: T {temp}°F, BP {bp_systolic}/{bp_diastolic}, HR {heart_rate}, RR {resp_rate}, O2 Sat {spo2}%
General: {general_appearance}
{system_exam}

### A (Assessment)
1. {primary_diagnosis}
2. {differential_diagnosis} (to rule out)
3. {chronic_condition} (pre-existing)

### P (Plan)
1. Medications: {med_plan}
2. Diagnostics: {diagnostic_plan}
3. Consultations: {consult_plan}
4. Patient Education: {education_plan}
5. Follow-up: {followup_plan}
        """
    ]
    
    # Variables for templating
    symptom_options = ["persistent cough", "lower back pain", "recurring headaches", "joint pain", "chest discomfort"]
    duration_options = ["the past 3 days", "approximately 2 weeks", "over a month", "several days", "about a week"]
    additional_complaint_options = [
        "Also notes fatigue", 
        "Reports difficulty sleeping", 
        "Mentions loss of appetite", 
        "Complains of nausea after eating",
        "Also experiencing mild dizziness"
    ]
    pain_description_options = [
        "dull and constant", 
        "sharp and intermittent", 
        "throbbing", 
        "burning",
        "aching that worsens with movement"
    ]
    medication_statement_options = [
        "Has been taking OTC ibuprofen with minimal relief",
        "Not currently taking any medications for symptoms",
        "Has tried acetaminophen with moderate relief",
        "Reports using prescription medication without improvement",
        "Has been using heating pad for comfort"
    ]
    
    # Generate random vitals within normal-ish ranges
    bp_systolic = random.randint(110, 140)
    bp_diastolic = random.randint(70, 90)
    heart_rate = random.randint(65, 95)
    resp_rate = random.randint(12, 20)
    temp = round(random.uniform(97.6, 99.4), 1)
    spo2 = random.randint(95, 99)
    
    physical_finding_options = [
        "tenderness to palpation in the right lower quadrant",
        "decreased range of motion in the lumbar spine",
        "erythema and swelling in the affected joint",
        "clear lung sounds bilaterally",
        "mild tenderness over the sinuses"
    ]
    
    additional_finding_options = [
        "No signs of neurological deficit.",
        "Mild edema noted in the extremities.",
        "Skin appears normal with no rash or lesions.",
        "Heart rhythm regular with no murmurs.",
        "No lymphadenopathy detected."
    ]
    
    diagnosis_options = [
        "Acute Bronchitis", 
        "Lumbar Strain", 
        "Tension Headache", 
        "Osteoarthritis", 
        "Gastroesophageal Reflux Disease"
    ]
    
    diagnosis_detail_options = [
        "likely viral in origin",
        "due to mechanical factors",
        "likely stress-related",
        "showing signs of progression",
        "moderately controlled"
    ]
    
    secondary_condition_options = [
        "Dehydration", 
        "Insomnia", 
        "Anxiety", 
        "Vitamin D Deficiency", 
        "Hypertension"
    ]
    
    relation_factor_options = [
        "recent lifestyle changes",
        "medication side effects",
        "underlying chronic condition",
        "poor dietary habits",
        "stress factors"
    ]
    
    medication_plan_options = [
        "Prescribed amoxicillin 500mg TID for 7 days",
        "Recommended ibuprofen 400mg q6h PRN for pain",
        "Started on omeprazole 20mg daily",
        "Prescribed cyclobenzaprine 10mg QHS for 5 days",
        "Recommended acetaminophen 500mg q6h PRN for pain and fever"
    ]
    
    followup_plan_options = [
        "Obtain chest X-ray to rule out pneumonia",
        "Complete blood count to check for infection markers",
        "Refer to physical therapy for evaluation and treatment",
        "Schedule for MRI of the affected area",
        "Advised to maintain food diary for two weeks"
    ]
    
    additional_recommendation_options = [
        "Increase fluid intake and rest",
        "Apply ice to affected area 20 minutes QID",
        "Elevate legs when sitting or lying down",
        "Perform recommended stretching exercises twice daily",
        "Avoid triggering foods such as spicy or acidic items"
    ]
    
    followup_timing_options = [
        "1 week", 
        "2 weeks", 
        "10 days", 
        "3-4 weeks", 
        "one month"
    ]
    
    # Additional variables for second template
    age = random.randint(25, 75)
    gender_options = ["male", "female"]
    gender = random.choice(gender_options)
    
    chief_complaint_options = ["severe headache", "shortness of breath", "abdominal pain", "dizziness", "chest pain"]
    chief_complaint = random.choice(chief_complaint_options)
    
    onset_time_options = ["yesterday", "two days ago", "this morning", "gradually over the past week", "suddenly while exercising"]
    onset_time = random.choice(onset_time_options)
    
    symptom_description_options = [
        "Pain is described as throbbing and radiates to the neck",
        "Reports feeling like can't get enough air, especially when lying down",
        "Describes pain as sharp and worse after eating",
        "States room feels like it's spinning, especially when standing",
        "Describes pain as crushing and radiating to left arm"
    ]
    symptom_description = random.choice(symptom_description_options)
    
    pain_level = random.randint(4, 8)
    
    history_element_options = [
        "Has history of similar episodes in the past",
        "No previous episodes reported",
        "Similar symptoms occurred last year",
        "First time experiencing these particular symptoms",
        "Symptoms have been getting progressively worse"
    ]
    history_element = random.choice(history_element_options)
    
    general_appearance_options = [
        "Alert and oriented x3, in mild distress",
        "Well-appearing, no acute distress",
        "Appears uncomfortable, shifting positions frequently",
        "Fatigued but alert and cooperative",
        "Mildly anxious but cooperative with exam"
    ]
    general_appearance = random.choice(general_appearance_options)
    
    system_exam_options = [
        "Cardiovascular: Regular rate and rhythm, no murmurs. Respiratory: Clear to auscultation bilaterally.",
        "HEENT: Mild pharyngeal erythema. Neck: No lymphadenopathy. Lungs: Clear to auscultation.",
        "Abdomen: Soft, tender in RLQ, no rebound or guarding. Bowel sounds active.",
        "Musculoskeletal: Limited ROM in lumbar spine, negative straight leg raise. Neurological: Intact sensation.",
        "Cardiovascular: Tachycardic but regular rhythm. Respiratory: Fine crackles in bilateral bases."
    ]
    system_exam = random.choice(system_exam_options)
    
    primary_diagnosis_options = [
        "Migraine without aura",
        "Community-acquired pneumonia",
        "Gastritis",
        "Benign paroxysmal positional vertigo",
        "Acute coronary syndrome"
    ]
    primary_diagnosis = random.choice(primary_diagnosis_options)
    
    differential_diagnosis_options = [
        "Tension headache", 
        "Bronchitis", 
        "Peptic ulcer disease", 
        "Labyrinthitis", 
        "Costochondritis"
    ]
    differential_diagnosis = random.choice(differential_diagnosis_options)
    
    chronic_condition_options = [
        "Hypertension",
        "Type 2 diabetes mellitus",
        "Asthma",
        "Osteoarthritis",
        "GERD"
    ]
    chronic_condition = random.choice(chronic_condition_options)
    
    med_plan_options = [
        "Start sumatriptan 50mg at onset of headache",
        "Amoxicillin 875mg BID for 7 days",
        "Pantoprazole 40mg daily before breakfast",
        "Meclizine 25mg TID PRN for dizziness",
        "Aspirin 325mg given in ED, continue 81mg daily"
    ]
    med_plan = random.choice(med_plan_options)
    
    diagnostic_plan_options = [
        "CBC, CMP ordered",
        "Chest X-ray completed, results pending",
        "EKG showed normal sinus rhythm",
        "CT head without contrast ordered",
        "Abdominal ultrasound scheduled"
    ]
    diagnostic_plan = random.choice(diagnostic_plan_options)
    
    consult_plan_options = [
        "Neurology consult requested",
        "Cardiology follow-up recommended",
        "Referral to gastroenterology",
        "ENT evaluation recommended",
        "None at this time"
    ]
    consult_plan = random.choice(consult_plan_options)
    
    education_plan_options = [
        "Discussed migraine triggers and avoidance",
        "Reviewed warning signs requiring return to ED",
        "Provided dietary recommendations",
        "Demonstrated Epley maneuver for home use",
        "Explained medication side effects"
    ]
    education_plan = random.choice(education_plan_options)
    
    followup_options = [
        "Follow up with PCP in 1 week",
        "Return to clinic in 3 days for recheck",
        "Schedule follow-up appointment in 2 weeks",
        "Return immediately if symptoms worsen",
        "Follow up with specialist within 5-7 days"
    ]
    followup = random.choice(followup_options)
    
    # Select a random template
    template = random.choice(mock_soap_templates)
    
    # Fill in the template with random values
    filled_template = template.format(
        symptom=random.choice(symptom_options),
        duration=random.choice(duration_options),
        additional_complaint=random.choice(additional_complaint_options),
        pain_description=random.choice(pain_description_options),
        medication_statement=random.choice(medication_statement_options),
        bp_systolic=bp_systolic,
        bp_diastolic=bp_diastolic,
        heart_rate=heart_rate,
        resp_rate=resp_rate,
        temp=temp,
        spo2=spo2,
        physical_finding=random.choice(physical_finding_options),
        additional_finding=random.choice(additional_finding_options),
        diagnosis=random.choice(diagnosis_options),
        diagnosis_detail=random.choice(diagnosis_detail_options),
        secondary_condition=random.choice(secondary_condition_options),
        relation_factor=random.choice(relation_factor_options),
        medication_plan=random.choice(medication_plan_options),
        followup_plan=random.choice(followup_plan_options),
        additional_recommendation=random.choice(additional_recommendation_options),
        followup_timing=random.choice(followup_timing_options),
        age=age,
        gender=gender,
        chief_complaint=chief_complaint,
        onset_time=onset_time,
        symptom_description=symptom_description,
        pain_level=pain_level,
        history_element=history_element,
        general_appearance=general_appearance,
        system_exam=system_exam,
        primary_diagnosis=primary_diagnosis,
        differential_diagnosis=differential_diagnosis,
        chronic_condition=chronic_condition,
        med_plan=med_plan,
        diagnostic_plan=diagnostic_plan,
        consult_plan=consult_plan,
        education_plan=education_plan,
    )
    
    return filled_template

def get_mock_structured_response(schema):
    """Generate mock structured response based on schema"""
    try:
        # Check if this is a SOAP schema (has subjective, objective, assessment, plan properties)
        properties = schema.get("properties", {})
        if all(key in properties for key in ["subjective", "objective", "assessment", "plan"]):
            return get_mock_structured_soap_response()
            
        # Check if this is a differential diagnosis array schema
        if schema.get("type") == "ARRAY" and schema.get("items", {}).get("properties", {}).get("condition"):
            return get_mock_structured_differential_diagnosis()
            
        # Handle other schema types
        result = {}
        
        # Handle risk assessment schema
        if "Risk" in properties:
            risk_options = properties["Risk"].get("enum", ["Low", "Medium", "High"])
            result["Risk"] = random.choice(risk_options)
            
        if "Condition" in properties:
            conditions = ["Hypertension", "Type 2 Diabetes", "Migraine", "Anxiety Disorder", 
                         "GERD", "Osteoarthritis", "Asthma", "Depression"]
            result["Condition"] = random.choice(conditions)
            
        if "Age" in properties:
            result["Age"] = random.randint(25, 80)
            
        if "LastVisit" in properties:
            # Generate a date within the last 3 months
            today = datetime.now()
            days_ago = random.randint(1, 90)
            last_visit = today - timedelta(days=days_ago)
            result["LastVisit"] = last_visit.strftime("%Y-%m-%d")
            
        # Return JSON string
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logging.error(f"Error generating mock structured response: {str(e)}")
        return json.dumps({"Error": "Failed to generate mock response"})

def get_mock_structured_soap_response():
    """Generate a structured SOAP response with arrays for each section"""
    # Generate a structured SOAP response
    soap_data = {
        "subjective": [
            f"Patient reports {random.choice(['headache', 'cough', 'fever', 'fatigue', 'back pain'])} for {random.randint(1, 10)} days.",
            f"Describes pain as {random.choice(['sharp', 'dull', 'throbbing', 'constant', 'intermittent'])}.",
            f"{random.choice(['No', 'Has'])} history of similar symptoms.",
            f"Currently taking {random.choice(['no medications', 'acetaminophen for pain', 'ibuprofen as needed', 'prescribed medications'])}."
        ],
        "objective": [
            f"Vital signs: BP {random.randint(110, 140)}/{random.randint(70, 90)}, HR {random.randint(60, 100)}, Temp {round(random.uniform(97.6, 102.5), 1)}°F, RR {random.randint(12, 20)}.",
            f"{random.choice(['Alert and oriented x3', 'Appears in mild distress', 'Well-appearing', 'Visibly uncomfortable'])}.",
            f"Physical exam: {random.choice(['Normal findings', 'Tenderness to palpation', 'Limited range of motion', 'Erythema noted', 'Auscultation reveals clear lungs'])}.",
            f"Labs: {random.choice(['WBC elevated at 12.3', 'CBC within normal limits', 'Pending', 'Not ordered'])}"
        ],
        "assessment": [
            f"{random.choice(['Acute upper respiratory infection', 'Migraine headache', 'Low back strain', 'Anxiety disorder', 'Gastroenteritis'])}.",
            f"{random.choice(['Likely viral in origin', 'Possibly aggravated by stress', 'Due to mechanical factors', 'Responding to current therapy'])}.",
            f"Differential includes {random.choice(['bacterial infection', 'tension headache', 'muscle spasm', 'panic attack', 'gastritis'])}."
        ],
        "plan": [
            f"{random.choice(['Rest and hydration', 'Continue current medications', 'Start new prescription', 'Physical therapy', 'Referral to specialist'])}.",
            f"Follow up in {random.choice(['1 week', '2 weeks', '1 month', '3 days if symptoms worsen'])}.",
            f"{random.choice(['Ordered lab tests', 'Scheduled imaging', 'Provided patient education', 'Recommended lifestyle modifications'])}.",
            f"Return precautions discussed."
        ]
    }
    
    return json.dumps(soap_data, indent=2)

def get_mock_structured_differential_diagnosis():
    """Generate a structured differential diagnosis response"""
    # Common conditions based on typical symptoms
    conditions = [
        {
            "name": "Upper Respiratory Infection",
            "risk_options": ["Low", "Moderate"],
            "confidence_range": (60, 90),
            "steps_options": [
                "Recommend symptomatic treatment with rest and hydration",
                "Advise over-the-counter pain relievers as needed for discomfort",
                "Follow up in 7-10 days if symptoms persist or worsen"
            ]
        },
        {
            "name": "Community-Acquired Pneumonia",
            "risk_options": ["Moderate"],
            "confidence_range": (40, 75),
            "steps_options": [
                "Order chest X-ray to confirm diagnosis",
                "Consider empiric antibiotic therapy with amoxicillin or doxycycline",
                "Assess oxygen saturation and consider supplemental oxygen if below 94%"
            ]
        },
        {
            "name": "Acute Bronchitis",
            "risk_options": ["Low", "Moderate"],
            "confidence_range": (50, 80),
            "steps_options": [
                "Recommend rest and increased fluid intake",
                "Consider bronchodilators if wheezing is present",
                "Educate on expected duration of cough (2-3 weeks)"
            ]
        },
        {
            "name": "Anxiety Disorder",
            "risk_options": ["Low", "Moderate"],
            "confidence_range": (40, 85),
            "steps_options": [
                "Administer GAD-7 screening tool",
                "Consider referral to mental health services",
                "Discuss stress management techniques and lifestyle modifications"
            ]
        },
        {
            "name": "Gastroesophageal Reflux Disease",
            "risk_options": ["Low"],
            "confidence_range": (55, 85),
            "steps_options": [
                "Recommend dietary modifications (avoid triggers, smaller meals)",
                "Trial of proton pump inhibitors for 2 weeks",
                "Elevate head of bed and avoid eating within 3 hours of bedtime"
            ]
        },
        {
            "name": "Acute Coronary Syndrome",
            "risk_options": ["Critical"],
            "confidence_range": (20, 60),
            "steps_options": [
                "Immediate ECG and cardiac enzyme testing",
                "Administer aspirin if not contraindicated",
                "Urgent cardiology consultation"
            ]
        },
        {
            "name": "Migraine",
            "risk_options": ["Low", "Moderate"],
            "confidence_range": (50, 90),
            "steps_options": [
                "Trial of sumatriptan or other triptan medication for acute relief",
                "Maintain headache diary to identify triggers",
                "Consider prophylactic therapy if episodes occur >4 times monthly"
            ]
        },
        {
            "name": "Viral Gastroenteritis",
            "risk_options": ["Low", "Moderate"],
            "confidence_range": (60, 95),
            "steps_options": [
                "Focus on oral rehydration therapy",
                "Monitor for signs of dehydration",
                "Symptomatic treatment with antiemetics if needed"
            ]
        }
    ]
    
    # Select 3-5 random conditions for the differential
    num_diagnoses = random.randint(3, 5)
    selected_conditions = random.sample(conditions, num_diagnoses)
    
    # Sort by confidence (descending)
    for condition in selected_conditions:
        condition["confidence"] = random.randint(condition["confidence_range"][0], condition["confidence_range"][1])
    
    selected_conditions.sort(key=lambda x: x["confidence"], reverse=True)
    
    # Format the response according to schema
    differential_diagnosis = []
    
    for condition in selected_conditions:
        diagnosis = {
            "condition": condition["name"],
            "risk": random.choice(condition["risk_options"]),
            "confidence": condition["confidence"],
            "steps": random.choice(condition["steps_options"])
        }
        differential_diagnosis.append(diagnosis)
    
    return json.dumps(differential_diagnosis, indent=2)

def get_mock_general_response():
    """Generate a general mock response"""
    responses = [
        "Based on the information provided, I recommend the patient follow up with their primary care physician for further evaluation.",
        "The symptoms described are consistent with a viral upper respiratory infection. Rest, hydration, and over-the-counter analgesics are recommended.",
        "From the medical history, this appears to be a case of mild to moderate anxiety that could benefit from cognitive behavioral therapy.",
        "The patient's description suggests possible gastroesophageal reflux disease. Dietary modifications and antacid therapy would be appropriate initial steps.",
        "These symptoms could indicate several conditions ranging from muscle strain to more serious issues. A physical examination is necessary for proper diagnosis."
    ]
    return random.choice(responses)
