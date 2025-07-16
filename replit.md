# Persian Bodybuilding Supplements E-commerce Store

## Overview

This is a Persian/Farsi e-commerce web application for bodybuilding supplements built with Flask. The application features a complete online store with product catalog, shopping cart, user authentication, and admin panel. It's designed with Persian language support and RTL (Right-to-Left) layout.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes (July 16, 2025)

### Major UI/UX Redesign
- ✓ Implemented modern design system with enhanced color palette and typography
- ✓ Added glassmorphism effects and advanced shadows for depth
- ✓ Created animated hero section with floating effects and gradient overlays  
- ✓ Enhanced product cards with hover animations and discount badges
- ✓ Added rating display system with star ratings
- ✓ Improved category cards with animated icons and gradient backgrounds
- ✓ Created modern statistics section showcasing store achievements
- ✓ Enhanced navigation with hover effects and backdrop blur
- ✓ Added responsive design improvements for mobile devices
- ✓ Implemented fade-in animations with staggered delays for better UX

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 RTL for responsive design
- **UI Framework**: Bootstrap 5 with RTL support for Persian language
- **Icons**: Font Awesome for consistent iconography
- **Styling**: Custom CSS with Persian fonts (Vazirmatn) and RTL-specific styles
- **JavaScript**: Vanilla JavaScript for interactive features

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Session Management**: Flask sessions for user authentication and cart persistence
- **Security**: Werkzeug for password hashing and security utilities
- **CORS**: Flask-CORS for cross-origin resource sharing
- **Authentication**: Custom decorators for login and admin access control

### Data Storage
- **Database**: JSON file-based storage system (no traditional database)
- **Data Files**: Separate JSON files for products, categories, orders, and users
- **Data Manager**: Custom utility class for JSON file operations

## Key Components

### Core Application (app.py)
- Main Flask application with route definitions
- Session-based user authentication
- Product catalog and shopping cart functionality
- Admin panel for store management

### Data Management (utils/data_manager.py)
- JSON file-based data persistence
- CRUD operations for products, categories, orders, and users
- File system organization in `/data` directory

### Authentication System (utils/auth.py)
- Login required decorator for protected routes
- Admin access control decorator
- Session-based user management

### Template System
- Base template with common layout and navigation
- Specialized templates for different sections (products, cart, admin, etc.)
- Persian language support with RTL layout

## Data Flow

1. **User Requests**: HTTP requests routed through Flask application
2. **Authentication**: Session-based user verification using custom decorators
3. **Data Access**: JSON files read/written through DataManager utility
4. **Template Rendering**: Jinja2 templates with data passed from Flask routes
5. **Client Response**: HTML pages with Bootstrap RTL styling and JavaScript enhancements

## External Dependencies

### Python Packages
- Flask: Web framework
- Flask-CORS: Cross-origin resource sharing
- Werkzeug: Security utilities and password hashing

### Frontend Libraries
- Bootstrap 5 RTL: UI framework with Persian language support
- Font Awesome: Icon library
- Google Fonts: Vazirmatn Persian font family

### Image Resources
- Pixabay: External image hosting for product images
- CDN-hosted CSS and JavaScript libraries

## Deployment Strategy

### Development Environment
- Local development server with debug mode enabled
- Port 5000 with host binding to 0.0.0.0
- Environment variables for configuration (SESSION_SECRET)

### File Structure
- Static files served from `/static` directory
- Templates located in `/templates` directory
- Data persistence in `/data` directory with JSON files
- Utility functions in `/utils` directory

### Session Management
- Server-side sessions using Flask's built-in session handling
- Session secret key configuration through environment variables
- Cart persistence through session storage

### Security Considerations
- Password hashing using Werkzeug security utilities
- Session-based authentication with custom decorators
- CORS configuration for API access
- Input validation and sanitization in forms

### Scalability Notes
- Current JSON file storage is suitable for small to medium stores
- Can be migrated to database system (PostgreSQL/MySQL) for larger scale
- Session storage can be moved to Redis for distributed deployments
- Static files can be moved to CDN for better performance

The application follows a simple but effective architecture suitable for a small to medium-sized e-commerce store with plans for future database integration and scaling.