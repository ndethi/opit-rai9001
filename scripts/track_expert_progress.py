#!/usr/bin/env python3
"""Track expert review progress and manage feedback collection for Kikuyu proverb validation."""

import pandas as pd
from pathlib import Path
import logging
from datetime import datetime, timedelta
import json
import argparse
from typing import Dict, List, Optional, Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ExpertReviewTracker:
    """Comprehensive expert review session management and progress tracking."""
    
    def __init__(self, tracking_file: str = "data/processed/expert_review/expert_tracking_template.xlsx"):
        """Initialize tracker with Excel file."""
        self.tracking_file = Path(tracking_file)
        self.expert_review_dir = self.tracking_file.parent
        self.expert_review_dir.mkdir(parents=True, exist_ok=True)
        
        # Load or create tracking data
        self._load_tracking_data()
        
        # Status workflow definitions
        self.status_workflow = {
            'Identified': ['Contacted', 'Declined'],
            'Contacted': ['Interested', 'No Response', 'Declined'],
            'Interested': ['Confirmed', 'Declined'],
            'Confirmed': ['In Progress', 'Declined'],
            'In Progress': ['Completed', 'Declined'],
            'Completed': [],  # Final state
            'Declined': [],   # Final state
            'No Response': ['Contacted', 'Declined']  # Can retry contact
        }
    
    def _load_tracking_data(self):
        """Load tracking data from Excel file."""
        if self.tracking_file.exists():
            try:
                self.experts_df = pd.read_excel(self.tracking_file, sheet_name='Expert_Tracking')
                self.communication_df = pd.read_excel(self.tracking_file, sheet_name='Communication_Log')
                self.progress_df = pd.read_excel(self.tracking_file, sheet_name='Review_Progress')
                self.instructions_df = pd.read_excel(self.tracking_file, sheet_name='Instructions')
                self.summary_df = pd.read_excel(self.tracking_file, sheet_name='Summary')
                logger.info(f"Loaded tracking data: {len(self.experts_df)} experts")
            except Exception as e:
                logger.error(f"Error loading tracking file: {e}")
                self._create_empty_dataframes()
        else:
            logger.warning("Tracking file not found. Creating new tracking system.")
            self._create_empty_dataframes()
    
    def _create_empty_dataframes(self):
        """Create empty DataFrames if file doesn't exist."""
        self.experts_df = pd.DataFrame(columns=[
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
        ])
        
        self.communication_df = pd.DataFrame(columns=[
            'Log_ID', 'Expert_ID', 'Expert_Name', 'Communication_Date',
            'Communication_Type', 'Contact_Method', 'Initiated_By',
            'Response_Received', 'Response_Date', 'Content_Summary',
            'Next_Action', 'Next_Action_Date', 'Status', 'Notes'
        ])
        
        self.progress_df = pd.DataFrame(columns=[
            'Expert_ID', 'Expert_Name', 'Total_Proverbs_Assigned',
            'Proverbs_Completed', 'Completion_Percentage',
            'Average_Time_Per_Proverb', 'Quality_Score_Average',
            'Cultural_Authenticity_Average', 'Business_Relevance_Average',
            'Last_Activity_Date', 'Estimated_Completion_Date',
            'Issues_Encountered', 'Support_Provided',
            'Session_1_Date', 'Session_1_Duration', 'Session_1_Proverbs',
            'Session_2_Date', 'Session_2_Duration', 'Session_2_Proverbs',
            'Session_3_Date', 'Session_3_Duration', 'Session_3_Proverbs',
            'Total_Review_Time', 'Notes'
        ])
        
        self.instructions_df = pd.DataFrame()
        self.summary_df = pd.DataFrame()
    
    def add_expert(self, name: str, email: str, expertise_area: str, 
                   title: str = "", institution: str = "", phone: str = "",
                   cultural_authority: str = "Moderate") -> str:
        """Add new expert to tracking system."""
        
        # Generate unique expert ID
        expert_count = len(self.experts_df) + 1
        expert_id = f"EXP{expert_count:03d}"
        
        # Ensure expert doesn't already exist
        if name in self.experts_df['Expert_Name'].values:
            logger.warning(f"Expert {name} already exists in tracking system")
            return self.experts_df[self.experts_df['Expert_Name'] == name]['Expert_ID'].iloc[0]
        
        new_expert = {
            'Expert_ID': expert_id,
            'Expert_Name': name,
            'Title_Role': title,
            'Institution_Community': institution,
            'Primary_Email': email,
            'Secondary_Email': '',
            'Phone': phone,
            'Preferred_Contact': 'Email',
            'Expertise_Area': expertise_area,
            'Cultural_Authority_Level': cultural_authority,
            'Academic_Background': '',
            'Business_Experience': '',
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
            'Notes': f"Added on {datetime.now().strftime('%Y-%m-%d')}",
            'Last_Updated': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        
        # Add to DataFrame
        new_expert_df = pd.DataFrame([new_expert])
        self.experts_df = pd.concat([self.experts_df, new_expert_df], ignore_index=True)
        
        # Initialize progress tracking
        progress_entry = {
            'Expert_ID': expert_id,
            'Expert_Name': name,
            'Total_Proverbs_Assigned': 96,  # Default assignment
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
            'Notes': 'Expert added - no progress yet'
        }
        
        progress_df = pd.DataFrame([progress_entry])
        self.progress_df = pd.concat([self.progress_df, progress_df], ignore_index=True)
        
        self.save_tracking()
        logger.info(f"Added expert: {name} ({expert_id})")
        return expert_id
    
    def update_expert_status(self, expert_identifier: str, new_status: str, 
                           notes: str = "", contact_method: str = "Email") -> bool:
        """Update expert status with workflow validation."""
        
        # Find expert (by ID or name)
        if expert_identifier.startswith('EXP'):
            expert_mask = self.experts_df['Expert_ID'] == expert_identifier
        else:
            expert_mask = self.experts_df['Expert_Name'] == expert_identifier
        
        if not expert_mask.any():
            logger.error(f"Expert not found: {expert_identifier}")
            return False
        
        expert_row = self.experts_df[expert_mask].iloc[0]
        current_status = expert_row['Recruitment_Status']
        
        # Validate status transition
        if new_status not in self.status_workflow.get(current_status, []):
            if new_status != current_status:  # Allow same status updates
                logger.warning(f"Invalid status transition: {current_status} -> {new_status}")
                print(f"Valid transitions from '{current_status}': {self.status_workflow.get(current_status, [])}")
                return False
        
        # Update status
        self.experts_df.loc[expert_mask, 'Recruitment_Status'] = new_status
        self.experts_df.loc[expert_mask, 'Last_Updated'] = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        if notes:
            current_notes = expert_row['Notes']
            updated_notes = f"{current_notes}; {datetime.now().strftime('%Y-%m-%d')}: {notes}"
            self.experts_df.loc[expert_mask, 'Notes'] = updated_notes
        
        # Handle specific status transitions
        if new_status == 'Contacted':
            self.experts_df.loc[expert_mask, 'Contact_Attempts'] = expert_row['Contact_Attempts'] + 1
        
        elif new_status == 'Confirmed':
            # Set materials sent date and deadline
            materials_date = datetime.now().strftime('%Y-%m-%d')
            deadline = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
            self.experts_df.loc[expert_mask, 'Materials_Sent_Date'] = materials_date
            self.experts_df.loc[expert_mask, 'Review_Deadline'] = deadline
        
        elif new_status == 'Interested':
            self.experts_df.loc[expert_mask, 'Initial_Response_Date'] = datetime.now().strftime('%Y-%m-%d')
            self.experts_df.loc[expert_mask, 'Interest_Level'] = 'High'
        
        elif new_status == 'Completed':
            self.experts_df.loc[expert_mask, 'Completion_Date'] = datetime.now().strftime('%Y-%m-%d')
            self.experts_df.loc[expert_mask, 'Payment_Status'] = 'Processing'
        
        # Log communication
        self._log_communication(
            expert_row['Expert_ID'],
            expert_row['Expert_Name'],
            f"Status Update: {current_status} -> {new_status}",
            contact_method,
            notes
        )
        
        self.save_tracking()
        logger.info(f"Updated {expert_row['Expert_Name']} status: {current_status} -> {new_status}")
        return True
    
    def _log_communication(self, expert_id: str, expert_name: str, 
                          comm_type: str, method: str, content: str):
        """Log communication with expert."""
        
        log_id = f"LOG{len(self.communication_df) + 1:03d}"
        
        comm_entry = {
            'Log_ID': log_id,
            'Expert_ID': expert_id,
            'Expert_Name': expert_name,
            'Communication_Date': datetime.now().strftime('%Y-%m-%d'),
            'Communication_Type': comm_type,
            'Contact_Method': method,
            'Initiated_By': 'Researcher',
            'Response_Received': 'No',
            'Response_Date': '',
            'Content_Summary': content,
            'Next_Action': 'Wait for response',
            'Next_Action_Date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'Status': 'Pending',
            'Notes': f"Logged at {datetime.now().strftime('%H:%M')}"
        }
        
        comm_df = pd.DataFrame([comm_entry])
        self.communication_df = pd.concat([self.communication_df, comm_df], ignore_index=True)
    
    def update_review_progress(self, expert_identifier: str, proverbs_completed: int, 
                             session_duration: str = "", issues: str = "") -> bool:
        """Update expert's review progress."""
        
        # Find expert in progress tracking
        if expert_identifier.startswith('EXP'):
            progress_mask = self.progress_df['Expert_ID'] == expert_identifier
        else:
            progress_mask = self.progress_df['Expert_Name'] == expert_identifier
        
        if not progress_mask.any():
            logger.error(f"Expert not found in progress tracking: {expert_identifier}")
            return False
        
        # Update progress
        progress_row = self.progress_df[progress_mask].iloc[0]
        total_assigned = progress_row['Total_Proverbs_Assigned']
        
        self.progress_df.loc[progress_mask, 'Proverbs_Completed'] = proverbs_completed
        self.progress_df.loc[progress_mask, 'Completion_Percentage'] = round(
            (proverbs_completed / total_assigned) * 100, 1
        )
        self.progress_df.loc[progress_mask, 'Last_Activity_Date'] = datetime.now().strftime('%Y-%m-%d')
        
        if issues:
            current_issues = progress_row['Issues_Encountered']
            updated_issues = f"{current_issues}; {datetime.now().strftime('%Y-%m-%d')}: {issues}"
            self.progress_df.loc[progress_mask, 'Issues_Encountered'] = updated_issues
        
        # Track session details
        session_num = self._get_next_session_number(progress_row)
        if session_num <= 3:
            session_date_col = f'Session_{session_num}_Date'
            session_duration_col = f'Session_{session_num}_Duration'
            session_proverbs_col = f'Session_{session_num}_Proverbs'
            
            self.progress_df.loc[progress_mask, session_date_col] = datetime.now().strftime('%Y-%m-%d')
            if session_duration:
                self.progress_df.loc[progress_mask, session_duration_col] = session_duration
            self.progress_df.loc[progress_mask, session_proverbs_col] = proverbs_completed
        
        self.save_tracking()
        logger.info(f"Updated progress for {progress_row['Expert_Name']}: {proverbs_completed}/{total_assigned} proverbs")
        return True
    
    def _get_next_session_number(self, progress_row) -> int:
        """Determine next session number for tracking."""
        if pd.isna(progress_row['Session_1_Date']) or progress_row['Session_1_Date'] == '':
            return 1
        elif pd.isna(progress_row['Session_2_Date']) or progress_row['Session_2_Date'] == '':
            return 2
        elif pd.isna(progress_row['Session_3_Date']) or progress_row['Session_3_Date'] == '':
            return 3
        else:
            return 4  # Additional session
    
    def get_overdue_experts(self) -> List[Dict]:
        """Get list of experts with overdue reviews."""
        today = datetime.now().date()
        overdue_experts = []
        
        for _, expert in self.experts_df.iterrows():
            if (expert['Recruitment_Status'] in ['Confirmed', 'In Progress'] and 
                expert['Review_Deadline'] and expert['Completion_Date'] == ''):
                
                try:
                    deadline = datetime.strptime(expert['Review_Deadline'], '%Y-%m-%d').date()
                    if today > deadline:
                        days_overdue = (today - deadline).days
                        overdue_experts.append({
                            'expert_id': expert['Expert_ID'],
                            'name': expert['Expert_Name'],
                            'email': expert['Primary_Email'],
                            'deadline': expert['Review_Deadline'],
                            'days_overdue': days_overdue,
                            'contact_attempts': expert['Contact_Attempts']
                        })
                except ValueError:
                    continue
        
        return overdue_experts
    
    def generate_status_report(self) -> Dict:
        """Generate comprehensive status report."""
        status_counts = self.experts_df['Recruitment_Status'].value_counts().to_dict()
        
        # Progress statistics
        completed_reviews = len(self.experts_df[self.experts_df['Recruitment_Status'] == 'Completed'])
        in_progress = len(self.experts_df[self.experts_df['Recruitment_Status'] == 'In Progress'])
        
        # Calculate average completion percentage for in-progress reviews
        in_progress_experts = self.progress_df[
            self.progress_df['Expert_ID'].isin(
                self.experts_df[self.experts_df['Recruitment_Status'] == 'In Progress']['Expert_ID']
            )
        ]
        
        avg_completion = 0
        if len(in_progress_experts) > 0:
            valid_percentages = in_progress_experts['Completion_Percentage'].dropna()
            if len(valid_percentages) > 0:
                avg_completion = valid_percentages.mean()
        
        # Quality metrics
        completed_experts = self.experts_df[self.experts_df['Recruitment_Status'] == 'Completed']
        avg_quality = 0
        avg_authenticity = 0
        
        if len(completed_experts) > 0:
            quality_scores = completed_experts['Review_Quality_Score'].dropna()
            auth_scores = completed_experts['Cultural_Authenticity_Rating'].dropna()
            
            if len(quality_scores) > 0:
                avg_quality = pd.to_numeric(quality_scores, errors='coerce').mean()
            if len(auth_scores) > 0:
                avg_authenticity = pd.to_numeric(auth_scores, errors='coerce').mean()
        
        report = {
            'total_experts': len(self.experts_df),
            'status_breakdown': status_counts,
            'completed_reviews': completed_reviews,
            'in_progress_reviews': in_progress,
            'average_completion_percentage': round(avg_completion, 1),
            'average_quality_score': round(avg_quality, 2) if avg_quality > 0 else 'N/A',
            'average_authenticity_score': round(avg_authenticity, 2) if avg_authenticity > 0 else 'N/A',
            'overdue_count': len(self.get_overdue_experts()),
            'report_generated': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        
        return report
    
    def save_tracking(self):
        """Save all tracking data to Excel file."""
        with pd.ExcelWriter(self.tracking_file, engine='openpyxl') as writer:
            self.experts_df.to_excel(writer, sheet_name='Expert_Tracking', index=False)
            self.communication_df.to_excel(writer, sheet_name='Communication_Log', index=False)
            self.progress_df.to_excel(writer, sheet_name='Review_Progress', index=False)
            
            if not self.instructions_df.empty:
                self.instructions_df.to_excel(writer, sheet_name='Instructions', index=False)
            
            # Update summary with current statistics
            report = self.generate_status_report()
            summary_data = [
                {'Metric': 'Total Experts', 'Value': report['total_experts']},
                {'Metric': 'Completed Reviews', 'Value': report['completed_reviews']},
                {'Metric': 'In Progress Reviews', 'Value': report['in_progress_reviews']},
                {'Metric': 'Overdue Reviews', 'Value': report['overdue_count']},
                {'Metric': 'Average Quality Score', 'Value': report['average_quality_score']},
                {'Metric': 'Average Authenticity Score', 'Value': report['average_authenticity_score']},
                {'Metric': 'Last Updated', 'Value': datetime.now().strftime('%Y-%m-%d %H:%M')}
            ]
            
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        logger.info(f"Tracking data saved to {self.tracking_file}")
    
    def print_status_summary(self):
        """Print formatted status summary."""
        report = self.generate_status_report()
        
        print("\n" + "="*60)
        print("EXPERT REVIEW TRACKING SUMMARY")
        print("="*60)
        print(f"📊 Total Experts: {report['total_experts']}")
        print(f"✅ Completed Reviews: {report['completed_reviews']}")
        print(f"🔄 In Progress: {report['in_progress_reviews']}")
        print(f"⚠️  Overdue: {report['overdue_count']}")
        print(f"📈 Average Completion: {report['average_completion_percentage']}%")
        print(f"⭐ Average Quality: {report['average_quality_score']}")
        print(f"🎯 Average Authenticity: {report['average_authenticity_score']}")
        
        print("\n📋 Status Breakdown:")
        for status, count in report['status_breakdown'].items():
            print(f"   • {status}: {count}")
        
        # Show overdue experts if any
        overdue = self.get_overdue_experts()
        if overdue:
            print(f"\n⚠️  OVERDUE EXPERTS ({len(overdue)}):")
            for expert in overdue:
                print(f"   • {expert['name']} - {expert['days_overdue']} days overdue")
        
        print(f"\n🕐 Report Generated: {report['report_generated']}")
        print("="*60)

def main():
    """Command-line interface for expert tracking."""
    parser = argparse.ArgumentParser(description='Expert Review Session Management')
    parser.add_argument('--action', choices=['add', 'update', 'progress', 'report', 'overdue'], 
                       required=True, help='Action to perform')
    parser.add_argument('--name', help='Expert name')
    parser.add_argument('--email', help='Expert email')
    parser.add_argument('--expertise', help='Expert expertise area')
    parser.add_argument('--status', help='New status for expert')
    parser.add_argument('--notes', help='Additional notes')
    parser.add_argument('--proverbs', type=int, help='Number of proverbs completed')
    parser.add_argument('--duration', help='Session duration')
    parser.add_argument('--tracking-file', default='data/processed/expert_review/expert_tracking_template.xlsx',
                       help='Path to tracking Excel file')
    
    args = parser.parse_args()
    
    # Initialize tracker
    tracker = ExpertReviewTracker(args.tracking_file)
    
    if args.action == 'add':
        if not args.name or not args.email or not args.expertise:
            print("Error: --name, --email, and --expertise are required for adding experts")
            return
        
        expert_id = tracker.add_expert(args.name, args.email, args.expertise)
        print(f"✅ Added expert: {args.name} ({expert_id})")
    
    elif args.action == 'update':
        if not args.name or not args.status:
            print("Error: --name and --status are required for status updates")
            return
        
        success = tracker.update_expert_status(args.name, args.status, args.notes or "")
        if success:
            print(f"✅ Updated {args.name} status to: {args.status}")
        else:
            print(f"❌ Failed to update {args.name}")
    
    elif args.action == 'progress':
        if not args.name or args.proverbs is None:
            print("Error: --name and --proverbs are required for progress updates")
            return
        
        success = tracker.update_review_progress(args.name, args.proverbs, 
                                               args.duration or "", args.notes or "")
        if success:
            print(f"✅ Updated {args.name} progress: {args.proverbs} proverbs completed")
        else:
            print(f"❌ Failed to update progress for {args.name}")
    
    elif args.action == 'report':
        tracker.print_status_summary()
    
    elif args.action == 'overdue':
        overdue = tracker.get_overdue_experts()
        if overdue:
            print(f"\n⚠️  OVERDUE EXPERTS ({len(overdue)}):")
            for expert in overdue:
                print(f"   • {expert['name']} ({expert['email']})")
                print(f"     Deadline: {expert['deadline']} ({expert['days_overdue']} days overdue)")
                print(f"     Contact attempts: {expert['contact_attempts']}")
                print()
        else:
            print("✅ No overdue experts!")

if __name__ == "__main__":
    main()