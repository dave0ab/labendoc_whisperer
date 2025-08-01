#!/usr/bin/env python3
"""
Easy-to-use custom vocabulary system
You can define everything here for your specific use case
"""

class CustomVocabulary:
    """
    Easy customization class - add your own terms here!
    """
    
    def __init__(self):
        # YOUR CUSTOM NAMES - Add any names you need
        self.custom_names = [
            "Reina", "Zaya", "Carlos", "Dave",
            # Add more names here:
            "Maria", "Jose", "Ana", "Luis", "Carmen", "Miguel",
            "Patricia", "Roberto", "Elena", "Fernando", "Sofia",
            # Your business contacts:
            # "YourClientName", "YourColleagueName", etc.
        ]
        
        # YOUR CUSTOM BUSINESS TERMS - Add your specific terminology
        self.custom_business_terms = [
            "project", "meeting", "client", "deadline", "budget",
            # Add your company-specific terms:
            # "YourCompanyName", "YourDepartment", "YourProducts", etc.
        ]
        
        # YOUR CUSTOM MEDICAL TERMS - Add your specific medical vocabulary
        self.custom_medical_terms = [
            "patient", "symptom", "diagnosis", "medication", "allergy",
            "prescription", "treatment", "fever", "headache", "nausea",
            # Spanish medical terms:
            "paciente", "síntoma", "diagnóstico", "medicamento", "alergia",
            "receta", "tratamiento", "fiebre", "dolor de cabeza", "náusea",
            # Add more specific medical terms for your use case:
            # "YourSpecialty", "SpecificConditions", etc.
        ]
        
        # YOUR CUSTOM CORRECTIONS - Fix specific transcription errors
        self.custom_corrections = {
            # Common phrase fixes
            "okay, ten, kid": "Good morning guys",
            "by role": "by mistake", 
            "at prode": "for the same purpose",
            "team work site": "work as a team",
            "locally": "Carlos",
            
            # Medical corrections
            "medico": "médico",
            "sintomas": "síntomas", 
            "diagnostico": "diagnóstico",
            
            # Business corrections
            "oficina": "oficina",
            "reunion": "reunión",
            "proyecto": "proyecto",
            
            # Add your specific corrections here:
            # "wrong_transcription": "correct_transcription",
            # "another_error": "correct_version",
        }
        
        # YOUR DOMAIN-SPECIFIC VOCABULARY
        self.domain_vocabulary = {
            # Healthcare domain
            "healthcare": [
                "clinic", "hospital", "pharmacy", "nurse", "doctor",
                "clínica", "hospital", "farmacia", "enfermera", "doctor"
            ],
            
            # Business domain  
            "business": [
                "contract", "invoice", "revenue", "profit", "marketing",
                "contrato", "factura", "ingresos", "ganancia", "mercadeo"
            ],
            
            # Technology domain
            "technology": [
                "software", "hardware", "database", "server", "network",
                "application", "platform", "system", "cloud", "security"
            ],
            
            # Add your specific domains:
            # "your_domain": ["term1", "term2", "term3"]
        }
    
    def get_all_names(self):
        """Get all custom names"""
        return self.custom_names
    
    def get_all_business_terms(self):
        """Get all business terms"""
        return self.custom_business_terms
    
    def get_all_medical_terms(self):
        """Get all medical terms"""
        return self.custom_medical_terms
    
    def get_all_corrections(self):
        """Get all correction mappings"""
        return self.custom_corrections
    
    def get_domain_vocabulary(self, domain=None):
        """Get vocabulary for specific domain"""
        if domain:
            return self.domain_vocabulary.get(domain, [])
        return self.domain_vocabulary
    
    def add_names(self, names):
        """Add new names to the vocabulary"""
        self.custom_names.extend(names)
    
    def add_business_terms(self, terms):
        """Add new business terms"""
        self.custom_business_terms.extend(terms)
    
    def add_medical_terms(self, terms):
        """Add new medical terms"""
        self.custom_medical_terms.extend(terms)
    
    def add_corrections(self, corrections_dict):
        """Add new correction mappings"""
        self.custom_corrections.update(corrections_dict)
    
    def add_domain_vocabulary(self, domain, terms):
        """Add vocabulary for a new domain"""
        if domain not in self.domain_vocabulary:
            self.domain_vocabulary[domain] = []
        self.domain_vocabulary[domain].extend(terms)

# Easy configuration functions for users
def add_my_names(names_list):
    """
    Easy function to add your specific names
    Example: add_my_names(["John", "Sarah", "Company Name"])
    """
    vocab = CustomVocabulary()
    vocab.add_names(names_list)
    return vocab

def add_my_business_terms(terms_list):
    """
    Easy function to add your business terminology
    Example: add_my_business_terms(["quarterly report", "board meeting"])
    """
    vocab = CustomVocabulary()
    vocab.add_business_terms(terms_list)
    return vocab

def add_my_corrections(corrections_dict):
    """
    Easy function to add your specific correction mappings
    Example: add_my_corrections({"wrong": "right", "error": "correct"})
    """
    vocab = CustomVocabulary()
    vocab.add_corrections(corrections_dict)
    return vocab

# EXAMPLE USAGE:
if __name__ == "__main__":
    # Example of how to customize for your needs
    
    # Create vocabulary instance
    vocab = CustomVocabulary()
    
    # Add your specific names
    my_team_names = ["Jennifer", "Michael", "Rodriguez", "Thompson"]
    vocab.add_names(my_team_names)
    
    # Add your business terms
    my_business_terms = ["quarterly review", "stakeholder meeting", "KPI dashboard"]
    vocab.add_business_terms(my_business_terms)
    
    # Add your specific corrections
    my_corrections = {
        "mistake_word": "correct_word",
        "another_error": "correct_version"
    }
    vocab.add_corrections(my_corrections)
    
    # Add domain-specific vocabulary
    vocab.add_domain_vocabulary("my_company", [
        "product_name", "department_name", "process_name"
    ])
    
    print("✅ Custom vocabulary configured!")
    print(f"Names: {len(vocab.get_all_names())}")
    print(f"Business terms: {len(vocab.get_all_business_terms())}")
    print(f"Medical terms: {len(vocab.get_all_medical_terms())}")
    print(f"Corrections: {len(vocab.get_all_corrections())}")
    print(f"Domains: {list(vocab.get_domain_vocabulary().keys())}")