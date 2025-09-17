#!/usr/bin/env python3
"""Generate expert tracking Excel template for Kikuyu proverb validation project."""

import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_expert_tracking_template():
    """Create comprehensive expert tracking Excel template."""
    
    # Create output directory
    output_dir = Path("data/processed/expert_review")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "expert_tracking_template.xlsx"
    
    # Expert tracking sheet structure
    expert_columns = [
        'Expert_ID', 'Expert_Name', 'Title_Role', 'Institution_Community',
        'Primary_Email', 'Secondary_Email', 'Phone', 'Preferred_Contact',
        'Expertise_Area', 'Cultural_Authority_Level', 'Academic_Background',
        'Business_Experience', 'Previous_Collaboration',
        'Date_Identified', 'Recruitment_Status', 'Contact_Attempts',
        'Initial_Response_Date', 'Interest_Level', 'Availability_Status',
        'Materials_Sent_Date', 'Review_Deadline', 'Extension_Granted',
        'Progress_Check_1', 'Progress_Check_2', 'Progress_Check_3',
        'Completion_Date', 'Review_Quality_Score', 'Cultural_Authenticity_Rating',
        'Response_Completeness', 'Follow_up_Required', 'Payment_Status',
        'Feedback_on_Process', 'Willing_Future_Collaboration', 'Notes',
        'Last_Updated'
    ]
    
    # Sample expert data for template
    sample_experts = [
        {
            'Expert_ID': 'EXP001',
            'Expert_Name': 'Dr. Jane Wanjiku',
            'Title_Role': 'Professor of African Languages',
            'Institution_Community': 'University of Nairobi',
            'Primary_Email': 'j.wanjiku@uonbi.ac.ke',
            'Secondary_Email': '',
            'Phone': '+254-XXX-XXXXXX',
            'Preferred_Contact': 'Email',
            'Expertise_Area': 'Kikuyu Linguistics & Cultural Studies',
            'Cultural_Authority_Level': 'High',
            'Academic_Background': 'PhD in African Languages',
            'Business_Experience': 'Limited',
            'Previous_Collaboration': 'None',
            'Date_Identified': datetime.now().strftime('%Y-%m-%d'),
            'Recruitment_Status': 'Identified',
            'Contact_Attempts': 0,
            'Initial_Response_Date': '',
            'Interest_Level': '',
            'Availability_Status': '',
            'Materials_Sent_Date': '',
            'Review_Deadline': '',
            'Extension_Granted': 'No',
            'Progress_Check_1': '',
            'Progress_Check_2': '',
            'Progress_Check_3': '',
            'Completion_Date': '',
            'Review_Quality_Score': '',
            'Cultural_Authenticity_Rating': '',
            'Response_Completeness': '',
            'Follow_up_Required': '',
            'Payment_Status': 'Pending',
            'Feedback_on_Process': '',
            'Willing_Future_Collaboration': '',
            'Notes': 'High priority - strong academic background',
            'Last_Updated': datetime.now().strftime('%Y-%m-%d %H:%M')
        },
        {
            'Expert_ID': 'EXP002',
            'Expert_Name': 'Mzee John Kariuki',
            'Title_Role': 'Community Elder & Business Leader',
            'Institution_Community': 'Nyeri Community Council',
            'Primary_Email': 'j.kariuki@gmail.com',
            'Secondary_Email': '',
            'Phone': '+254-XXX-XXXXXX',
            'Preferred_Contact': 'Phone',
            'Expertise_Area': 'Traditional Business Wisdom',
            'Cultural_Authority_Level': 'Very High',
            'Academic_Background': 'Traditional Education',
            'Business_Experience': 'Extensive',
            'Previous_Collaboration': 'None',
            'Date_Identified': datetime.now().strftime('%Y-%m-%d'),
            'Recruitment_Status': 'Identified',
            'Contact_Attempts': 0,
            'Initial_Response_Date': '',
            'Interest_Level': '',
            'Availability_Status': '',
            'Materials_Sent_Date': '',
            'Review_Deadline': '',
            'Extension_Granted': 'No',
            'Progress_Check_1': '',
            'Progress_Check_2': '',
            'Progress_Check_3': '',
            'Completion_Date': '',
            'Review_Quality_Score': '',
            'Cultural_Authenticity_Rating': '',
            'Response_Completeness': '',
            'Follow_up_Required': '',
            'Payment_Status': 'Pending',
            'Feedback_on_Process': '',
            'Willing_Future_Collaboration': '',
            'Notes': 'Strong business context - community respected',
            'Last_Updated': datetime.now().strftime('%Y-%m-%d %H:%M')
        },
        {
            'Expert_ID': 'EXP003',
            'Expert_Name': 'Prof. Mary Muthoni',
            'Title_Role': 'Cultural Anthropologist',
            'Institution_Community': 'Institute for Cultural Studies',
            'Primary_Email': 'm.muthoni@ics.ac.ke',
            'Secondary_Email': 'mary.muthoni@gmail.com',
            'Phone': '+254-XXX-XXXXXX',
            'Preferred_Contact': 'Email',
            'Expertise_Area': 'Cultural Anthropology & Proverb Studies',
            'Cultural_Authority_Level': 'High',
            'Academic_Background': 'PhD in Cultural Anthropology',
            'Business_Experience': 'Moderate',
            'Previous_Collaboration': 'Research collaboration 2020',
            'Date_Identified': datetime.now().strftime('%Y-%m-%d'),
            'Recruitment_Status': 'Identified',
            'Contact_Attempts': 0,
            'Initial_Response_Date': '',
            'Interest_Level': '',
            'Availability_Status': '',
            'Materials_Sent_Date': '',
            'Review_Deadline': '',
            'Extension_Granted': 'No',
            'Progress_Check_1': '',
            'Progress_Check_2': '',
            'Progress_Check_3': '',
            'Completion_Date': '',
            'Review_Quality_Score': '',
            'Cultural_Authenticity_Rating': '',
            'Response_Completeness': '',
            'Follow_up_Required': '',
            'Payment_Status': 'Pending',
            'Feedback_on_Process': '',
            'Willing_Future_Collaboration': '',
            'Notes': 'Previous collaboration - reliable and thorough',
            'Last_Updated': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
    ]
    
    # Create main tracking DataFrame
    experts_df = pd.DataFrame(sample_experts)
    
    # Communication log structure
    comm_log_data = [
        {
            'Log_ID': 'LOG001',
            'Expert_ID': 'EXP001',
            'Expert_Name': 'Dr. Jane Wanjiku',
            'Communication_Date': datetime.now().strftime('%Y-%m-%d'),
            'Communication_Type': 'Initial Email',
            'Contact_Method': 'Email',
            'Initiated_By': 'Researcher',
            'Response_Received': 'No',
            'Response_Date': '',
            'Content_Summary': 'Initial recruitment email sent with project overview',
            'Next_Action': 'Wait for response (7 days)',
            'Next_Action_Date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'Status': 'Pending Response',
            'Notes': 'Used recruitment template - professional tone'
        }
    ]
    
    comm_log_df = pd.DataFrame(comm_log_data)
    
    # Review progress tracking
    progress_data = [
        {
            'Expert_ID': 'EXP001',
            'Expert_Name': 'Dr. Jane Wanjiku',
            'Total_Proverbs_Assigned': 96,
            'Proverbs_Completed': 0,
            'Completion_Percentage': 0,
            'Average_Time_Per_Proverb': '',
            'Quality_Score_Average': '',
            'Cultural_Authenticity_Average': '',
            'Business_Relevance_Average': '',
            'Last_Activity_Date': '',
            'Estimated_Completion_Date': '',
            'Issues_Encountered': '',
            'Support_Provided': '',
            'Session_1_Date': '',
            'Session_1_Duration': '',
            'Session_1_Proverbs': '',
            'Session_2_Date': '',
            'Session_2_Duration': '',
            'Session_2_Proverbs': '',
            'Session_3_Date': '',
            'Session_3_Duration': '',
            'Session_3_Proverbs': '',
            'Total_Review_Time': '',
            'Notes': 'Template entry - no progress yet'
        }
    ]
    
    progress_df = pd.DataFrame(progress_data)
    
    # Instructions and guidelines
    instructions_data = [
        {
            'Section': 'Expert_Status_Codes',
            'Code': 'Identified',
            'Description': 'Expert identified as potential reviewer'
        },
        {
            'Section': 'Expert_Status_Codes',
            'Code': 'Contacted',
            'Description': 'Initial contact made'
        },
        {
            'Section': 'Expert_Status_Codes',
            'Code': 'Interested',
            'Description': 'Expressed interest in participating'
        },
        {
            'Section': 'Expert_Status_Codes',
            'Code': 'Confirmed',
            'Description': 'Agreed to participate, materials sent'
        },
        {
            'Section': 'Expert_Status_Codes',
            'Code': 'In Progress',
            'Description': 'Currently reviewing proverbs'
        },
        {
            'Section': 'Expert_Status_Codes',
            'Code': 'Completed',
            'Description': 'Finished review process'
        },
        {
            'Section': 'Expert_Status_Codes',
            'Code': 'Declined',
            'Description': 'Declined to participate'
        },
        {
            'Section': 'Expert_Status_Codes',
            'Code': 'No Response',
            'Description': 'No response after follow-ups'
        },
        {
            'Section': 'Quality_Ratings',
            'Code': '1',
            'Description': 'Poor - Requires significant improvement'
        },
        {
            'Section': 'Quality_Ratings',
            'Code': '2',
            'Description': 'Fair - Some improvements needed'
        },
        {
            'Section': 'Quality_Ratings',
            'Code': '3',
            'Description': 'Good - Meets basic requirements'
        },
        {
            'Section': 'Quality_Ratings',
            'Code': '4',
            'Description': 'Very Good - High quality work'
        },
        {
            'Section': 'Quality_Ratings',
            'Code': '5',
            'Description': 'Excellent - Exceptional quality'
        },
        {
            'Section': 'Cultural_Authority_Levels',
            'Code': 'Very High',
            'Description': 'Recognized community elder or cultural leader'
        },
        {
            'Section': 'Cultural_Authority_Levels',
            'Code': 'High',
            'Description': 'Academic expert or respected community member'
        },
        {
            'Section': 'Cultural_Authority_Levels',
            'Code': 'Moderate',
            'Description': 'Some cultural knowledge and community standing'
        },
        {
            'Section': 'Cultural_Authority_Levels',
            'Code': 'Limited',
            'Description': 'Basic cultural knowledge'
        }
    ]
    
    instructions_df = pd.DataFrame(instructions_data)
    
    # Create Excel file with multiple sheets
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Main expert tracking sheet
        experts_df.to_excel(writer, sheet_name='Expert_Tracking', index=False)
        
        # Communication log
        comm_log_df.to_excel(writer, sheet_name='Communication_Log', index=False)
        
        # Progress tracking
        progress_df.to_excel(writer, sheet_name='Review_Progress', index=False)
        
        # Instructions and codes
        instructions_df.to_excel(writer, sheet_name='Instructions', index=False)
        
        # Summary statistics (placeholder)
        summary_data = [
            {'Metric': 'Total Experts Identified', 'Value': len(experts_df)},
            {'Metric': 'Experts Contacted', 'Value': 0},
            {'Metric': 'Confirmed Participants', 'Value': 0},
            {'Metric': 'Reviews in Progress', 'Value': 0},
            {'Metric': 'Completed Reviews', 'Value': 0},
            {'Metric': 'Average Completion Time', 'Value': 'TBD'},
            {'Metric': 'Overall Quality Score', 'Value': 'TBD'},
            {'Metric': 'Template Created Date', 'Value': datetime.now().strftime('%Y-%m-%d %H:%M')}
        ]
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    logger.info(f"Expert tracking template created: {output_file}")
    return output_file

if __name__ == "__main__":
    template_file = create_expert_tracking_template()
    print(f"✅ Expert tracking Excel template created: {template_file}")
    print("📋 Template includes:")
    print("   • Expert_Tracking - Main expert information and status")
    print("   • Communication_Log - All communication records")
    print("   • Review_Progress - Review session tracking") 
    print("   • Instructions - Status codes and guidelines")
    print("   • Summary - Project statistics")