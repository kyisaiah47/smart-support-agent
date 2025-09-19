"""
Sample data for CloudFlow SaaS customer support knowledge base
"""

KNOWLEDGE_BASE_DATA = [
    {
        "id": "kb_001",
        "title": "How to reset your password",
        "content": "To reset your password: 1) Go to login page 2) Click 'Forgot Password' 3) Enter your email 4) Check your email for reset link 5) Follow the link and create new password. If you don't receive the email, check spam folder or contact support.",
        "category": "account",
        "tags": ["password", "login", "account"],
        "confidence_score": 0.95
    },
    {
        "id": "kb_002",
        "title": "Understanding billing cycles",
        "content": "CloudFlow bills monthly on the date you signed up. Pro plans are $29/month, Team plans are $99/month. Billing includes all features for that tier. You can upgrade/downgrade anytime. Refunds are prorated for downgrades.",
        "category": "billing",
        "tags": ["billing", "pricing", "subscription"],
        "confidence_score": 0.98
    },
    {
        "id": "kb_003",
        "title": "Integrating with Slack",
        "content": "To integrate with Slack: 1) Go to Settings > Integrations 2) Click 'Add Slack' 3) Authorize CloudFlow in Slack 4) Choose which channels get notifications 5) Configure notification preferences. You can receive updates for project milestones, task assignments, and due dates.",
        "category": "integrations",
        "tags": ["slack", "integration", "notifications"],
        "confidence_score": 0.92
    },
    {
        "id": "kb_004",
        "title": "Troubleshooting slow dashboard loading",
        "content": "If your dashboard loads slowly: 1) Clear browser cache and cookies 2) Disable browser extensions 3) Try incognito/private mode 4) Check your internet connection 5) Try a different browser. For persistent issues, contact support with your browser version and connection speed.",
        "category": "technical",
        "tags": ["performance", "dashboard", "browser"],
        "confidence_score": 0.88
    },
    {
        "id": "kb_005",
        "title": "Managing team permissions",
        "content": "Team permissions in CloudFlow: Admin (full access), Manager (edit projects, manage team), Member (view and edit assigned tasks), Viewer (read-only). To change permissions: Go to Team > Members > Click user > Select role. Only Admins can promote other Admins.",
        "category": "team_management",
        "tags": ["permissions", "team", "roles"],
        "confidence_score": 0.94
    },
    {
        "id": "kb_006",
        "title": "Canceling your subscription",
        "content": "To cancel: 1) Go to Account > Billing 2) Click 'Cancel Subscription' 3) Choose cancellation reason 4) Confirm cancellation. Your account remains active until the end of current billing period. Data is retained for 30 days after cancellation for reactivation.",
        "category": "billing",
        "tags": ["cancel", "subscription", "billing"],
        "confidence_score": 0.96
    },
    {
        "id": "kb_007",
        "title": "Exporting project data",
        "content": "Export options: 1) Go to Project > Settings > Export 2) Choose format (CSV, PDF, JSON) 3) Select date range 4) Click Export. Large exports are emailed as download links. Exports include tasks, comments, time tracking, and file attachments.",
        "category": "data_management",
        "tags": ["export", "data", "backup"],
        "confidence_score": 0.90
    },
    {
        "id": "kb_008",
        "title": "Setting up two-factor authentication",
        "content": "Enable 2FA: 1) Go to Account > Security 2) Click 'Enable 2FA' 3) Scan QR code with authenticator app 4) Enter verification code 5) Save backup codes. Supported apps: Google Authenticator, Authy, 1Password. Contact support if you lose access.",
        "category": "security",
        "tags": ["2fa", "security", "authentication"],
        "confidence_score": 0.97
    }
]

SUPPORT_TICKETS_DATA = [
    {
        "id": "ticket_001",
        "ticket_id": "CF-2024-001",
        "problem": "Cannot access my account after password reset",
        "solution": "User was entering old password. Guided through proper reset process and cleared browser cache. Issue resolved.",
        "category": "account",
        "priority": "high",
        "resolution_time": 15,
        "satisfaction_score": 4.5,
        "created_date": "2024-01-15T10:30:00Z"
    },
    {
        "id": "ticket_002",
        "ticket_id": "CF-2024-002",
        "problem": "Charged twice for the same month",
        "solution": "Duplicate charge due to payment method update. Refunded duplicate charge within 3-5 business days. Updated billing system to prevent future occurrences.",
        "category": "billing",
        "priority": "medium",
        "resolution_time": 45,
        "satisfaction_score": 4.8,
        "created_date": "2024-01-16T14:20:00Z"
    },
    {
        "id": "ticket_003",
        "ticket_id": "CF-2024-003",
        "problem": "Slack integration not working, notifications not appearing",
        "solution": "Integration token expired. Re-authorized Slack connection and updated webhook URLs. Tested notifications successfully.",
        "category": "integrations",
        "priority": "medium",
        "resolution_time": 25,
        "satisfaction_score": 4.2,
        "created_date": "2024-01-17T09:15:00Z"
    },
    {
        "id": "ticket_004",
        "ticket_id": "CF-2024-004",
        "problem": "Dashboard takes 30+ seconds to load",
        "solution": "Large dataset causing performance issues. Implemented pagination for task lists and optimized database queries. Loading time reduced to under 3 seconds.",
        "category": "technical",
        "priority": "high",
        "resolution_time": 120,
        "satisfaction_score": 4.7,
        "created_date": "2024-01-18T16:45:00Z"
    },
    {
        "id": "ticket_005",
        "ticket_id": "CF-2024-005",
        "problem": "Team member cannot see shared projects",
        "solution": "User had Viewer permissions instead of Member. Updated permissions and explained role differences. User can now access and edit shared projects.",
        "category": "team_management",
        "priority": "medium",
        "resolution_time": 10,
        "satisfaction_score": 4.9,
        "created_date": "2024-01-19T11:30:00Z"
    }
]

PRODUCT_CATALOG_DATA = [
    {
        "id": "product_001",
        "product_name": "CloudFlow Free",
        "description": "Basic project management for individuals and small teams. Up to 3 projects, 5 team members.",
        "features": ["Basic task management", "File sharing", "Calendar view", "Mobile app"],
        "limitations": ["3 project limit", "5 team member limit", "Basic integrations only"],
        "troubleshooting": "Free accounts have limited storage (1GB). Upgrade to Pro for unlimited storage.",
        "price": "$0/month"
    },
    {
        "id": "product_002",
        "product_name": "CloudFlow Pro",
        "description": "Professional project management with advanced features. Unlimited projects and team members.",
        "features": ["Advanced task management", "Time tracking", "Custom fields", "API access", "Advanced integrations"],
        "limitations": ["No white-label options", "Standard support only"],
        "troubleshooting": "Pro features may take 24 hours to activate after upgrade. Contact support if delayed.",
        "price": "$29/month"
    },
    {
        "id": "product_003",
        "product_name": "CloudFlow Team",
        "description": "Enterprise-grade project management with team collaboration tools and priority support.",
        "features": ["Everything in Pro", "White-label options", "Priority support", "Advanced analytics", "SSO integration"],
        "limitations": ["Minimum 10 users"],
        "troubleshooting": "Enterprise features require admin setup. Dedicated onboarding specialist assigned.",
        "price": "$99/month"
    }
]