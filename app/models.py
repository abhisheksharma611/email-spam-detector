"""
Advanced Email Classification System for Spam Detection
"""
import re
import string
from collections import Counter

class EmailClassifier:
    """Advanced Email Classification System with Custom Risk Levels"""
    
    def __init__(self):
        # Enhanced classification categories with better keywords
        self.categories = {
            'spam': {
                'keywords': ['free', 'money', 'cash', 'winner', 'lottery', 'congratulations', 
                           'urgent', 'act now', 'limited time', 'guaranteed', 'bonus', 
                           'win', 'prize', 'claim', 'inheritance', 'million', 'dollars', 
                           'viagra', 'pills', 'weight loss', 'make money fast', 'earn money'],
                'weight': 3.0,
                'display_name': 'Spam',
                'color': '#dc3545',
                'icon': '⚠️'
            },
            'not_spam': {
                'keywords': ['meeting', 'schedule', 'regards', 'best', 'thank you', 'please', 
                           'project', 'work', 'team', 'update', 'sincerely', 'business', 
                           'attached', 'report', 'deadline', 'conference', 'colleague'],
                'weight': 1.0,
                'display_name': 'Not Spam',
                'color': '#28a745',
                'icon': '✅'
            },
            'promotional': {
                'keywords': ['sale', 'discount', 'offer', 'promotion', 'coupon', 'save', 
                           'special', 'exclusive', 'deal', 'shop now', 'buy', 'store',
                           'black friday', 'cyber monday', 'clearance', 'markdown'],
                'weight': 2.0,
                'display_name': 'Promotional',
                'color': '#fd7e14',
                'icon': '🏷️'
            },
            'phishing': {
                'keywords': ['verify account', 'suspended', 'security alert', 'update payment',
                           'confirm identity', 'account locked', 'expires today', 'click here immediately',
                           'immediate action', 'suspended account', 'security breach', 'verify now',
                           'update billing', 'confirm details'],
                'weight': 4.0,
                'display_name': 'Phishing',
                'color': '#dc3545',
                'icon': '🎣'
            },
            'newsletter': {
                'keywords': ['newsletter', 'subscribe', 'unsubscribe', 'monthly', 'weekly',
                           'updates', 'news', 'insights', 'industry', 'publication', 'digest',
                           'edition', 'issue', 'article', 'blog post'],
                'weight': 1.0,
                'display_name': 'Newsletter',
                'color': '#17a2b8',
                'icon': '📰'
            },
            'social': {
                'keywords': ['friend request', 'notification', 'tagged', 'liked', 'shared',
                           'comment', 'follow', 'connect', 'facebook', 'instagram', 'twitter',
                           'linkedin', 'social media', 'profile', 'post'],
                'weight': 1.5,
                'display_name': 'Social',
                'color': '#6f42c1',
                'icon': '👥'
            }
        }
        
        # Enhanced pattern detection
        self.patterns = {
            'money_amounts': r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?',
            'percentages': r'\d+%\s*(?:off|discount|save)',
            'urgency': r'\b(?:urgent|immediate|expires?|hurry|act now|limited time|final notice)\b',
            'caps_words': r'\b[A-Z]{4,}\b',
            'multiple_exclamation': r'!{2,}',
            'suspicious_phrases': r'\b(?:click here|act now|limited time|expires today|verify now)\b',
            'business_formal': r'\b(?:dear|sincerely|regards|meeting|schedule|attached)\b',
            'social_words': r'\b(?:like|share|follow|friend|connect|tag)\b'
        }
    
    def analyze_email(self, email_text):
        """Improved email analysis with custom risk levels"""
        if not email_text or not email_text.strip():
            return self._create_result('unknown', 0.0, {}, [], {})
        
        # Clean and prepare text
        clean_text = self._clean_text(email_text)
        original_text = email_text.lower()
        
        # Extract features
        features = self._extract_features(email_text)
        
        # Multi-algorithm classification
        keyword_scores = self._keyword_classification(clean_text)
        pattern_scores = self._pattern_classification(original_text)
        context_scores = self._context_classification(original_text, features)
        
        # Combine all scoring methods
        final_scores = self._intelligent_score_combination(
            keyword_scores, pattern_scores, context_scores, features
        )
        
        # Determine primary category and confidence
        primary_category = max(final_scores.items(), key=lambda x: x[1])[0]
        confidence = final_scores[primary_category]
        
        # Find specific indicators
        indicators = self._find_indicators(email_text)
        
        return self._create_result(primary_category, confidence, final_scores, indicators, features)
    
    def _create_result(self, category, confidence, scores, indicators, features):
        """Create formatted result dictionary"""
        category_info = self.categories.get(category, {
            'display_name': 'Unknown',
            'color': '#6c757d',
            'icon': '❓'
        })
        
        # Format scores for display
        formatted_scores = []
        for cat, score in scores.items():
            cat_info = self.categories.get(cat, {'display_name': cat.title(), 'color': '#6c757d'})
            formatted_scores.append({
                'category': cat,
                'display_name': cat_info['display_name'],
                'score': round(score * 100, 1),
                'color': cat_info['color']
            })
        
        formatted_scores.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'category': category,
            'display_name': category_info['display_name'],
            'confidence': round(confidence * 100, 2),
            'color': category_info['color'],
            'icon': category_info['icon'],
            'scores': formatted_scores,
            'risk_level': self._assess_risk(category, confidence, features),
            'indicators': indicators,
            'features': features
        }
    
    def _clean_text(self, text):
        """Clean and normalize text"""
        text = text.lower()
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _extract_features(self, text):
        """Extract detailed email features"""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        
        features = {
            'char_count': len(text),
            'word_count': len(words),
            'sentence_count': len([s for s in sentences if s.strip()]),
            'avg_word_length': sum(len(word) for word in words) / max(len(words), 1),
            'exclamation_count': text.count('!'),
            'question_count': text.count('?'),
            'caps_ratio': sum(1 for c in text if c.isupper()) / max(len(text), 1),
            'url_count': len(re.findall(r'https?://\S+|www\.\S+', text)),
            'email_addresses': len(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)),
            'phone_numbers': len(re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text)),
            'money_mentions': len(re.findall(self.patterns['money_amounts'], text))
        }
        
        return features
    
    def _keyword_classification(self, clean_text):
        """Enhanced keyword-based classification"""
        scores = {category: 0.0 for category in self.categories.keys()}
        
        for category, data in self.categories.items():
            category_score = 0
            keywords = data['keywords']
            weight = data['weight']
            
            for keyword in keywords:
                if keyword in clean_text:
                    frequency = clean_text.count(keyword)
                    context_bonus = 1.5 if len(keyword.split()) > 1 else 1.0
                    category_score += weight * frequency * context_bonus
            
            scores[category] = min(category_score / 20.0, 1.0)
        
        return scores
    
    def _pattern_classification(self, text):
        """Enhanced pattern-based classification"""
        scores = {category: 0.0 for category in self.categories.keys()}
        
        # Spam patterns
        if re.search(self.patterns['money_amounts'], text):
            scores['spam'] += 0.4
            scores['promotional'] += 0.2
        
        if re.search(self.patterns['urgency'], text):
            scores['spam'] += 0.5
            scores['phishing'] += 0.6
        
        if re.search(self.patterns['multiple_exclamation'], text):
            scores['spam'] += 0.3
            scores['promotional'] += 0.2
        
        # Business patterns
        if re.search(self.patterns['business_formal'], text):
            scores['not_spam'] += 0.4
            scores['newsletter'] += 0.2
        
        # Social patterns
        if re.search(self.patterns['social_words'], text):
            scores['social'] += 0.5
        
        # Newsletter patterns
        if any(word in text for word in ['newsletter', 'unsubscribe', 'edition']):
            scores['newsletter'] += 0.4
        
        return scores
    
    def _context_classification(self, text, features):
        """Context-based classification"""
        scores = {category: 0.0 for category in self.categories.keys()}
        
        # Professional email indicators
        professional_indicators = ['dear', 'sincerely', 'regards', 'best wishes', 'thank you']
        professional_count = sum(1 for indicator in professional_indicators if indicator in text)
        
        if professional_count >= 2:
            scores['not_spam'] += 0.4
        elif professional_count >= 1:
            scores['not_spam'] += 0.2
        
        # Spam structure indicators
        if features['exclamation_count'] > 5 or features['caps_ratio'] > 0.3:
            scores['spam'] += 0.4
        
        if features['money_mentions'] > 0:
            scores['spam'] += 0.3
            scores['promotional'] += 0.2
        
        # Newsletter structure
        if features['word_count'] > 100 and 'unsubscribe' in text:
            scores['newsletter'] += 0.5
        
        # Social media structure
        social_terms = ['notification', 'friend', 'like', 'share', 'follow']
        social_count = sum(1 for term in social_terms if term in text)
        if social_count >= 2:
            scores['social'] += 0.4
        
        return scores
    
    def _intelligent_score_combination(self, keyword_scores, pattern_scores, context_scores, features):
        """Intelligently combine scores"""
        combined = {category: 0.0 for category in self.categories.keys()}
        
        # Weighted combination
        for category in self.categories.keys():
            combined[category] = (
                keyword_scores[category] * 0.4 +
                pattern_scores[category] * 0.4 +
                context_scores[category] * 0.2
            )
        
        # Ensure minimum threshold for not_spam
        if all(score < 0.2 for score in combined.values()):
            combined['not_spam'] = 0.7
        
        # Normalize scores
        total = sum(combined.values())
        if total > 0:
            combined = {k: v / total for k, v in combined.items()}
        
        return combined
    
    def _assess_risk(self, category, confidence, features):
        """
        CUSTOM RISK LEVELS BY CATEGORY AND PERCENTAGE!
        Modify these percentages to change when HIGH/MEDIUM/LOW risk appears
        """
        
        # 🎯 CUSTOMIZE THESE PERCENTAGES FOR EACH CATEGORY:
        risk_thresholds = {
            'spam': {
                'high': 70,    # 70%+ confidence = HIGH risk
                'medium': 40,  # 40-69% confidence = MEDIUM risk
                'low': 0       # Below 40% = LOW risk
            },
            'phishing': {
                'high': 60,    # 60%+ confidence = HIGH risk (more sensitive)
                'medium': 30,  # 30-59% confidence = MEDIUM risk
                'low': 0       # Below 30% = LOW risk
            },
            'promotional': {
                'high': 85,    # 85%+ confidence = HIGH risk
                'medium': 50,  # 50-84% confidence = MEDIUM risk
                'low': 0       # Below 50% = LOW risk
            },
            'not_spam': {
                'high': 95,    # 95%+ confidence = HIGH risk (very safe)
                'medium': 80,  # 80-94% confidence = MEDIUM risk
                'low': 0       # Below 80% = LOW risk
            },
            'newsletter': {
                'high': 90,    # 90%+ confidence = HIGH risk
                'medium': 60,  # 60-89% confidence = MEDIUM risk
                'low': 0       # Below 60% = LOW risk
            },
            'social': {
                'high': 80,    # 80%+ confidence = HIGH risk
                'medium': 50,  # 50-79% confidence = MEDIUM risk
                'low': 0       # Below 50% = LOW risk
            }
        }
        
        # Get thresholds for this category
        thresholds = risk_thresholds.get(category, risk_thresholds['spam'])
        
        # Convert confidence to percentage if needed
        confidence_percent = confidence * 100 if confidence <= 1 else confidence
        
        # Determine risk level based on confidence thresholds
        if confidence_percent >= thresholds['high']:
            return 'high'
        elif confidence_percent >= thresholds['medium']:
            return 'medium'
        else:
            return 'low'
    
    def _find_indicators(self, text):
        """Find specific warning indicators"""
        indicators = []
        
        warning_checks = {
            'Money Amount': self.patterns['money_amounts'],
            'Urgency Words': self.patterns['urgency'],
            'Excessive Caps': self.patterns['caps_words'],
            'Multiple Exclamations': self.patterns['multiple_exclamation'],
            'Suspicious Links': self.patterns['suspicious_phrases']
        }
        
        for indicator_name, pattern in warning_checks.items():
            if re.search(pattern, text, re.IGNORECASE):
                indicators.append(indicator_name)
        
        # Additional manual checks
        if text.count('!') > 5:
            indicators.append('Excessive Punctuation')
        
        if len(re.findall(r'https?://\S+', text)) > 2:
            indicators.append('Multiple URLs')
        
        return list(set(indicators))

# Global classifier instance
email_classifier = EmailClassifier()
