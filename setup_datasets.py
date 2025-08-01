#!/usr/bin/env python3
"""
Setup script to download and configure all datasets
"""
from advanced_accuracy import AdvancedAccuracyEngine
from custom_vocabulary import CustomVocabulary

def setup_all_datasets():
    """Setup all datasets and vocabularies"""
    
    print("🚀 Setting up Advanced Transcription Accuracy System")
    print("=" * 60)
    
    # Initialize the advanced accuracy engine
    engine = AdvancedAccuracyEngine()
    
    # Download all datasets
    print("\n📥 DOWNLOADING LARGE DATASETS...")
    print("-" * 40)
    
    # This will download medical, business, and names datasets
    engine.initialize_all_datasets()
    
    # Initialize custom vocabulary
    print("\n🎯 SETTING UP CUSTOM VOCABULARY...")
    print("-" * 40)
    
    vocab = CustomVocabulary()
    
    # Add custom vocabularies to the engine
    engine.add_custom_vocabulary(vocab.get_all_names(), "names")
    engine.add_custom_vocabulary(vocab.get_all_medical_terms(), "medical") 
    engine.add_custom_vocabulary(vocab.get_all_business_terms(), "business")
    engine.add_custom_corrections(vocab.get_all_corrections())
    
    # Add domain vocabularies
    for domain, terms in vocab.get_domain_vocabulary().items():
        engine.add_custom_vocabulary(terms, domain)
    
    print("\n✅ SETUP COMPLETE!")
    print("=" * 40)
    
    # Show statistics
    total_medical = len(engine.medical_vocab)
    total_names = len(engine.names_vocab) 
    total_business = len(engine.business_vocab)
    total_corrections = len(engine.corrections_dict)
    total_vocab = total_medical + total_names + total_business
    
    print(f"📊 Dataset Statistics:")
    print(f"• Medical terms: {total_medical:,}")
    print(f"• Names: {total_names:,}")
    print(f"• Business terms: {total_business:,}")
    print(f"• Custom corrections: {total_corrections:,}")
    print(f"• Total vocabulary: {total_vocab:,}")
    
    print(f"\n💡 Your transcription service now has:")
    print(f"✅ {total_vocab:,} vocabulary terms for perfect recognition")
    print(f"✅ {total_corrections:,} custom corrections for your specific use case")
    print(f"✅ Downloadable datasets that auto-update")
    print(f"✅ Easy customization in custom_vocabulary.py")
    
    print(f"\n🎯 How to customize for YOUR needs:")
    print(f"1. Edit custom_vocabulary.py - add your names, terms, corrections")
    print(f"2. Run this script again to update")
    print(f"3. Restart your server")
    print(f"4. Enjoy perfect transcriptions!")
    
    return True

def add_your_custom_data():
    """Example of how to add your specific data"""
    
    print(f"\n🔧 EXAMPLE: Adding your custom data")
    print("-" * 40)
    
    engine = AdvancedAccuracyEngine()
    
    # Example: Add your team names
    your_team_names = [
        "Jennifer", "Michael", "Sarah", "David", "Maria", 
        "Rodriguez", "Johnson", "Williams", "Brown", "Davis"
        # Add your actual team names here
    ]
    
    # Example: Add your company-specific terms
    your_business_terms = [
        "quarterly review", "stakeholder meeting", "KPI dashboard",
        "project milestone", "deliverable", "action item", "follow-up",
        # Add your company's specific terminology
    ]
    
    # Example: Add your specific correction mappings
    your_corrections = {
        "q1": "Q1",
        "q2": "Q2", 
        "q3": "Q3",
        "q4": "Q4",
        "kpi": "KPI",
        "roi": "ROI",
        "ceo": "CEO",
        "cto": "CTO",
        # Add your specific corrections
    }
    
    # Add to the engine
    engine.add_custom_vocabulary(your_team_names, "names")
    engine.add_custom_vocabulary(your_business_terms, "business")
    engine.add_custom_corrections(your_corrections)
    
    print(f"✅ Added {len(your_team_names)} team names")
    print(f"✅ Added {len(your_business_terms)} business terms")
    print(f"✅ Added {len(your_corrections)} corrections")
    
    print(f"\n💡 To add YOUR data:")
    print(f"1. Edit the lists above with your actual data")
    print(f"2. Or edit custom_vocabulary.py for permanent changes")
    print(f"3. Run this script to apply changes")

if __name__ == "__main__":
    setup_all_datasets()
    add_your_custom_data()
    
    print(f"\n🎉 Ready! Your transcription service is now supercharged!")
    print(f"Test it at: http://127.0.0.1:8000")