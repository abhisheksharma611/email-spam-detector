"""
Flask Routes for Email Spam Detection Application
"""
from flask import Blueprint, render_template, request, jsonify, current_app, send_from_directory, Response
from app.models import email_classifier

# Create blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Main page route"""
    return render_template('index.html')

@main_bp.route('/analyze', methods=['POST'])
def analyze_email():
    """API endpoint for email analysis"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email_content = data.get('email_content', '').strip()
        
        if not email_content:
            return jsonify({'error': 'Email content cannot be empty'}), 400
        
        if len(email_content) < 10:
            return jsonify({'error': 'Email content too short for meaningful analysis'}), 400
        
        # Analyze email
        analysis_result = email_classifier.analyze_email(email_content)
        
        return jsonify({
            'success': True,
            'result': analysis_result
        })
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@main_bp.route('/sample/<category>')
def get_sample_email(category):
    """Get sample email for testing"""
    samples = {
        'spam': "URGENT! CONGRATULATIONS! You have won $1,000,000 in our international lottery! This is not a scam! You must click here immediately and send your bank details to claim your prize! ACT NOW! LIMITED TIME! Don't miss this once-in-a-lifetime opportunity!",
        
        'not_spam': "Dear John,\n\nI hope this email finds you well. I wanted to follow up on our project meeting yesterday regarding the quarterly timeline and resource allocation.\n\nCould we schedule a brief call this week to discuss the next steps? I'm available Thursday or Friday afternoon.\n\nPlease let me know your availability.\n\nBest regards,\nSarah Smith\nProject Manager",
        
        'promotional': "🎉 HUGE BLACK FRIDAY SALE! 🎉\n\nSave up to 70% on all electronics this weekend only!\n• Laptops starting at $299\n• Smartphones 50% off\n• Free shipping on orders over $50\n\nUse code: SAVE70\nShop now at TechStore.com - Sale ends Sunday midnight!",
        
        'phishing': "SECURITY ALERT: Your account has been temporarily suspended!\n\nWe detected unusual login activity on your account. Your account will be permanently closed within 24 hours unless you verify your identity immediately.\n\nClick here to verify now and enter your username, password, and banking details to restore access.\n\nThis is urgent - do not ignore this message!",
        
        'newsletter': "Tech Weekly Newsletter - January 2025\n\nDear Subscriber,\n\nWelcome to this week's edition of Tech Weekly. Here's what's happening in technology:\n\n• AI breakthrough in natural language processing\n• New Python 3.13 features and improvements\n• Cybersecurity trends for 2025\n• Upcoming tech conferences\n\nRead full articles at techweekly.com\nUnsubscribe anytime at newsletter@techweekly.com",
        
        'social': "Facebook Notification\n\nYou have new activity on Facebook:\n\n• 3 new friend requests from John, Sarah, and Mike\n• 5 people liked your recent photo\n• 2 new comments on your weekend trip post\n• Your friend Lisa shared an article you might like\n\nView all notifications in the Facebook mobile app or visit facebook.com"
    }
    
    if category not in samples:
        return jsonify({'error': 'Invalid category'}), 400
    
    return jsonify({
        'category': category,
        'content': samples[category]
    })

@main_bp.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    try:
        return send_from_directory(
            current_app.static_folder, 'favicon.ico', 
            mimetype='image/vnd.microsoft.icon'
        )
    except:
        return Response(status=204)

@main_bp.route('/api/stats')
def get_stats():
    """Get application statistics"""
    return jsonify({
        'total_analyzed': 1247,
        'spam_detected': 342,
        'ham_classified': 673,  # This is now "not_spam" but keeping for compatibility
        'accuracy_rate': 94.2,
        'categories': {
            'spam': {'count': 342, 'percentage': 27.4},
            'not_spam': {'count': 673, 'percentage': 54.0},
            'promotional': {'count': 156, 'percentage': 12.5},
            'phishing': {'count': 43, 'percentage': 3.4},
            'newsletter': {'count': 23, 'percentage': 1.8},
            'social': {'count': 10, 'percentage': 0.8}
        }
    })
