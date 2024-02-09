import re
import urllib.request
import spacy


nlp = spacy.load('en_core_web_md')

regex_patterns = {
    'email_pattern': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
    'phone_pattern': r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
    'link_pattern': r'\b(?:https?://|www\.)\S+\b'
}

class TextClean:
    
    def remove_email_phone_links(text: str):
        for pattern in regex_patterns:
            text = re.sub(regex_patterns[pattern], '', text)
        return text
    
    def clean_text(text: str):
        text = TextClean.remove_email_phone_links(text)
        doc = nlp(text)
        for token in doc:
            if token.pos_ == 'PUNCT':
                text = text.replace(token.text, '')
        return str(text)
    
    def remove_stopwords(text: str):
        doc = nlp(text)
        for token in doc:
            if token.is_stop:
                text = text.replace(token.text, '')
        return text
    
RESUME_SECTIONS = [
    'Contact Information',
    'Objective',
    'Summary',
    'Education',
    'Experience',
    'Skills',
    'Projects',
    'Certifications',
    'Licenses',
    'Awards',
    'Honors',
    'Publications',
    'References',
    'Technical Skills',
    'Computer Skills',
    'Programming Languages',
    'Software Skills',
    'Soft Skills',
    'Language Skills',
    'Professional Skills',
    'Transferable Skills',
    'Work Experience',
    'Professional Experience',
    'Employment History',
    'Internship Experience',
    'Volunteer Experience',
    'Leadership Experience',
    'Research Experience',
    'Teaching Experience'
]

class DataExtractor:

    def __init__(self, raw_text: str):
        self.text = raw_text
        self.clean_text = TextClean.clean_text(self.text)
        self.doc = nlp(self.clean_text)

    def extract_links(self):
        link_pattern = r'\b(?:https?://|www\.)\S+\b'
        links = re.findall(link_pattern, self.text)
        return links
    
    
    def extract_names(self):
        names = [ent.text for ent in self.doc.ents if ent.label_ == 'PERSON']
        return names
    
    def extract_emails(self):
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
        emails = re.findall(email_pattern, self.text)
        return emails
    
    def extract_phone_numbers(self):
        phone_number_pattern = r'\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*'
        matches = re.findall(phone_number_pattern,self.text)
        phone_numbers = []
        for match in matches:
            phone_number = '-'.join(filter(None, match))
            phone_numbers.append(phone_number)
        return "".join(phone_numbers)
    
    def extract_experience(self):
        experience_section = []
        in_experience_section = False

        for token in self.doc:
            if token.text in RESUME_SECTIONS:
                if token.text == 'Experience' or 'EXPERIENCE' or 'experience':
                    in_experience_section = True
                else:
                    in_experience_section = False

            if in_experience_section:
                experience_section.append(token.text)

        return " ".join(experience_section)
    
    def extract_position_year(self):
        position_year_search_pattern = r"(\b\w+\b\s+\b\w+\b),\s+(\d{4})\s*-\s*(\d{4}|\bpresent\b)"
        position_year = re.findall(position_year_search_pattern, self.text)
        return position_year
        
    def extract_particular_words(self):
        pos_tags = ['NOUN', 'PROPN']    
        nouns = [token.text for token in self.doc if token.pos_ in pos_tags]
        return nouns
        
    def extract_entities(self):
        entity_labels = ['GPE', 'ORG']
        entities = [token.text for token in self.doc.ents if token.label_ in entity_labels]
        return list(set(entities))
    

class ParseResume:

    def __init__(self, resume: str):
        self.resume_data = resume
        self.clean_data = TextClean.clean_text(
            self.resume_data)
        self.entities = DataExtractor(self.clean_data).extract_entities()
        self.name = DataExtractor(self.clean_data[:30]).extract_names()
        self.experience = DataExtractor(self.clean_data).extract_experience()
        self.emails = DataExtractor(self.resume_data).extract_emails()
        self.phones = DataExtractor(self.resume_data).extract_phone_numbers()
        self.years = DataExtractor(self.clean_data).extract_position_year()

        
    def get_JSON(self) -> dict:
        """
        Returns a dictionary of resume data.
        """
        resume_dictionary = {
            "resume_data": self.resume_data,
            "clean_data": self.clean_data,
            "entities": self.entities,
            "name": self.name,
            "experience": self.experience,
            "emails": self.emails,
            "phones": self.phones,
            "years": self.years,
        }

        return resume_dictionary