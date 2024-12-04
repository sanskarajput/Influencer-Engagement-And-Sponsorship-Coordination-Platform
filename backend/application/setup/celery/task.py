from celery import shared_task
from .mail import send_email
import calendar, random
from datetime import datetime
import csv
from io import StringIO


###################################
from application.setup.models import Influencers, AdRequests,Users,db, Campaigns, Sponsors
def generate_reminder_email(influencer_name, pending_requests_count=None):
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pending Ad Requests - Action Required</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .container {{
            background-color: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header {{
            background-color: #007bff;
            color: white;
            text-align: center;
            padding: 15px;
            border-radius: 8px 8px 0 0;
        }}
        .content {{
            margin-top: 20px;
        }}
        .cta-buttons {{
            display: flex;
            justify-content: center;
            gap: 15px;
            margin: 25px 0;
        }}
        .btn {{
            display: inline-block;
            padding: 12px 24px;
            background-color: #28a745;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
        }}
        .btn-secondary {{
            background-color: #17a2b8;
        }}
        .reasons {{
            background-color: #f8f9fa;
            border-radius: 5px;
            padding: 15px;
            margin: 20px 0;
        }}
        .footer {{
            text-align: center;
            color: #6c757d;
            font-size: 0.9em;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Ad Requests Waiting</h1>
        </div>
        
        <div class="content">
            <p>Dear {influencer_name},</p>
            
            <p>We noticed {f"you have {pending_requests_count} pending ad requests" if pending_requests_count else "you have pending ad requests"} waiting for your attention. 
            To keep your account active and maximize your opportunities, please take action soon.</p>
            
            <div class="cta-buttons">
                <a href="http://localhost:8080/dashboard/my-requests" class="btn">Review Requests</a>
                <a href="http://localhost:8080/dashboard/all-campaigns" class="btn btn-secondary">View Public Campaigns</a>
            </div>
            
            <div class="reasons">
                <h3>Why Act Now?</h3>
                <ul>
                    <li>Stay connected with top brands</li>
                    <li>Maximize your earning potential</li>
                    <li>Keep your profile actively engaged</li>
                </ul>
            </div>
            
            <p>Action Steps:</p>
            <ol>
                <li>Log in to your dashboard</li>
                <li>Review pending ad requests</li>
                <li>Accept or decline requests</li>
            </ol>
        </div>
        
        <div class="footer">
            <p>Need help? Contact our support team.</p>
            <p>&copy; 2024 Influencer Platform. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html_template

@shared_task(ignore_result=False)
def sending_mail_to_influencers_if_they_have_pending_request():
    From = Users.query.filter(Users.id == 1).first().email
    base_query = db.session.query(
        Influencers.id.label('influencer_id'),
        Users.id.label('user_id'),
        Users.email.label('email'),
        Users.name.label('name'),
        Users.username.label('username'),
        ).join(Users, Influencers.user_id == Users.id)\
         .join(AdRequests, Influencers.id == AdRequests.influencer_id)\
         .filter(AdRequests.status == 'PENDING')
    
    influencers_with_pending_requests = base_query.all()

    for influencer in influencers_with_pending_requests:
        send_email(From, influencer.email, 'Pending Requests Reminder', generate_reminder_email(influencer.name))
    
    return 'All Pending Requests Reminder Email Sent to Influencer\' Successfully !'
###################################





###################################
def generate_monthly_report(sponsor):
        """
        Generate a comprehensive monthly report for a sponsor
        
        :param sponsor: Sponsor object
        :return: Dictionary with report details
        """
        current_year = datetime.now().year
        current_month = datetime.now().month
        first_day_of_month = datetime(current_year, current_month, 1)
        last_day_of_month = datetime(current_year, current_month, calendar.monthrange(current_year, current_month)[1])
        
        # Fetch campaigns for the sponsor
        base_query = db.session.query(
            Campaigns
        ).join(Sponsors, Campaigns.creater_id_which_is_a_sponsor == Sponsors.id)\
         .filter(Campaigns.time.between(first_day_of_month, last_day_of_month),)

        
        campaigns = base_query.all()
        # Aggregate campaign metrics
        total_campaigns = len(campaigns)
        total_budget = sponsor.budget or 0
        spent_budget = sum(campaign.budget for campaign in campaigns) or 0
        total_impressions = random.choice([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])*random.choice([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
        total_clicks = random.choice([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])*random.choice([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
        total_conversions = random.choice([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])*random.choice([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
        total_estimated_sales = random.choice([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])*random.choice([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
        
        # Prepare report context
        report_context = {
            'sponsor_name': sponsor.user.name,
            'sponsor_type': sponsor.typee or 'N/A',
            'report_month': datetime.now().strftime('%B %Y'),
            'total_campaigns': total_campaigns,
            'total_budget': total_budget,
            'spent_budget': spent_budget,
            'remaining_budget': total_budget - spent_budget,
            'budget_utilization_percentage': (spent_budget / total_budget * 100) if total_budget else 0,
            'total_impressions': total_impressions,
            'total_clicks': total_clicks,
            'total_conversions': total_conversions,
            'estimated_sales_impact': total_estimated_sales,
            'campaigns': []
        }
        
        # Detailed campaign information
        for campaign in campaigns:
            report_context['campaigns'].append({
                'name': campaign.name,
                'visibility': 'campaign.visibility',
                'budget': 345345,
                'spent': 1000,
                'impressions': 499,
                'clicks': 212,
                'conversions': 234,
                'estimated_sales': 345
            })
        
        return report_context


def generate_report_email(report_context):
        """
        Generate HTML email for monthly report
        
        :param report_context: Report data dictionary
        :return: Email content dictionary
        """
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monthly Campaign Report - {report_context['report_month']}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .container {{
            background-color: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header {{
            background-color: #007bff;
            color: white;
            text-align: center;
            padding: 15px;
            border-radius: 8px 8px 0 0;
        }}
        .summary-section {{
            display: flex;
            justify-content: space-between;
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .summary-item {{
            text-align: center;
            flex: 1;
        }}
        .campaigns-section {{
            margin-top: 20px;
        }}
        .campaign-card {{
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 15px;
        }}
        .cta-button {{
            display: block;
            width: 200px;
            margin: 20px auto;
            padding: 12px 24px;
            background-color: #28a745;
            color: white;
            text-decoration: none;
            text-align: center;
            border-radius: 5px;
        }}
        .no-campaigns {{
            text-align: center;
            color: #6c757d;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Monthly Campaign Report - {report_context['report_month']}</h1>
        </div>
        
        <div class="summary-section">
            <div class="summary-item">
                <h3>Total Campaigns</h3>
                <p>{report_context['total_campaigns']}</p>
            </div>
            <div class="summary-item">
                <h3>Total Budget</h3>
                <p>${report_context['total_budget']:,.2f}</p>
            </div>
            <div class="summary-item">
                <h3>Budget Utilized</h3>
                <p>{report_context['budget_utilization_percentage']:.2f}%</p>
            </div>
        </div>
        
        {''.join([f"""
        <div class="campaigns-section">
            {''.join([f'''
            <div class="campaign-card">
                <h2>{campaign['name']}</h2>
                <p><strong>Visibility:</strong> {campaign['visibility']}</p>
                <p><strong>Budget:</strong> ${campaign['budget']:,.2f}</p>
                <p><strong>Spent:</strong> ${campaign['spent']:,.2f}</p>
                <p><strong>Impressions:</strong> {campaign['impressions']}</p>
                <p><strong>Clicks:</strong> {campaign['clicks']}</p>
                <p><strong>Conversions:</strong> {campaign['conversions']}</p>
                <p><strong>Estimated Sales Impact:</strong> ${campaign['estimated_sales']:,.2f}</p>
            </div>
            ''' for campaign in report_context['campaigns']])}
        </div>
        """] if report_context['campaigns'] else [f"""
        <div class="no-campaigns">
            <h2>No Active Campaigns</h2>
            <p>It looks like you don't have any active campaigns this month.</p>
            <a href="#" class="cta-button">Create New Campaign</a>
        </div>
        """])}
        
        <div style="text-align: center; margin-top: 20px;">
            <p>Need help? Contact our support team.</p>
        </div>
    </div>
</body>
</html>
"""
        
        return {
            'subject': f'Monthly Campaign Report - {report_context["report_month"]}',
            'content_body': html_template,
        }


@shared_task(ignore_result=False)
def monthly_report_for_sponsors_of_their_campaign():
    From = Users.query.filter(Users.id == 1).first().email
    sponsors = Sponsors.query.all()

    for sponsor in sponsors:
        report_context = generate_monthly_report(sponsor)
        email_content = generate_report_email(report_context)

        send_email(From, sponsor.user.email, **email_content)


    return 'Monthly Report of Campaigns to their Sponsors Sent Successfully !'
###################################



###################################
@shared_task(ignore_result=False)
def create_csv():
   # Query all campaigns
    campaigns = Campaigns.query.all()

    # Create an in-memory file
    output = StringIO()
    writer = csv.writer(output)

    # Write the CSV header
    writer.writerow([
        'ID',
        'Name',
        'Sponsor',
        'Category',
        'Budget',
        'Start Date',
        'End Date',
        'Visibility',
        'Time',
        'Flagged',
        'Goals',
        'Description'
        ])

    # Write data rows
    for campaign in campaigns:
        writer.writerow([
            campaign.id,
            campaign.name,
            campaign.campaigner.user.name,
            campaign.category,
            campaign.budget,
            campaign.start_date,
            campaign.end_date,
            campaign.visibility,
            campaign.time,
            campaign.flagged,
            campaign.goals,
            campaign.description
        ])

    # Get the CSV data as a string
    csv_data = output.getvalue()
    output.close()

    # Return the CSV content
    return csv_data
###################################
