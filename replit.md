# Overview

ERHAN is a modern, web-based visitor registration system designed for businesses to track and manage visitor entries and exits. The application provides a comprehensive solution for recording visitor information, managing user access, and generating reports. Built with a mobile-responsive design, it supports both desktop and mobile usage with a clean, professional interface.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The frontend is built using React with TypeScript, leveraging modern development practices:
- **Component Framework**: React 18 with functional components and hooks
- **State Management**: TanStack Query for server state and React Context for global app state
- **UI Framework**: Radix UI components with shadcn/ui design system
- **Styling**: Tailwind CSS with CSS variables for theming
- **Routing**: Wouter for lightweight client-side routing
- **Forms**: React Hook Form with Zod validation schemas
- **Build Tool**: Vite for fast development and optimized production builds

## Backend Architecture
The backend follows a REST API architecture pattern:
- **Runtime**: Node.js with Express.js framework
- **Language**: TypeScript with ES modules
- **Session Management**: Express sessions with PostgreSQL store for user authentication
- **Password Security**: bcrypt for password hashing
- **API Design**: RESTful endpoints with proper HTTP status codes and error handling

## Data Storage Solutions
- **Database**: PostgreSQL as the primary database
- **ORM**: Drizzle ORM for type-safe database operations
- **Hosting**: Neon Database for serverless PostgreSQL hosting
- **Migrations**: Drizzle Kit for database schema management
- **Connection Pooling**: Connection pooling for efficient database connections

## Database Schema Design
The system uses two main entities:
- **Users Table**: Stores user credentials, roles (user/admin/superadmin), and personal information
- **Visitors Table**: Records visitor information including entry/exit times, company details, and visit types
- **Relationships**: Foreign key relationship between visitors and the user who registered them

## Authentication and Authorization
- **Session-based Authentication**: Server-side sessions with PostgreSQL storage
- **Role-based Access Control**: Three user roles with different permission levels
  - Regular users: Can create and manage their own visitor records
  - Admins: Can manage users and access all visitor records
  - Superadmin: Special hardcoded admin account with full system access
- **Route Protection**: Middleware-based authentication checks on both client and server
- **Password Requirements**: Secure password hashing with bcrypt

## User Interface Design
- **Design System**: Modern, professional interface using shadcn/ui components
- **Theme Support**: Dark/light mode toggle with system preference detection
- **Responsive Design**: Mobile-first approach with desktop optimization
- **Accessibility**: Proper ARIA labels and keyboard navigation support
- **Internationalization**: Turkish language support throughout the interface

## Features and Functionality
- **Visitor Registration**: Form-based visitor entry with validation
- **Real-time Dashboard**: Today's visitors with statistics and quick actions
- **Search and Filtering**: Advanced search capabilities with date ranges and filters
- **Exit Time Management**: One-click exit time recording for active visitors
- **Excel Integration**: Import/export functionality for visitor data
- **User Management**: Admin interface for creating and managing user accounts

## Development and Deployment
- **Development Environment**: Hot module replacement with Vite dev server
- **Code Quality**: TypeScript for type safety, ESLint for code standards
- **Build Process**: Optimized production builds with code splitting
- **Deployment**: Vercel-compatible build configuration
- **Environment Variables**: Secure configuration management for database and session secrets

# External Dependencies

## Database Services
- **Neon Database**: Serverless PostgreSQL hosting with connection pooling
- **@neondatabase/serverless**: Official Neon database driver for serverless environments

## Authentication & Security
- **bcrypt**: Password hashing library for secure user authentication
- **express-session**: Session management middleware
- **connect-pg-simple**: PostgreSQL session store for persistent sessions

## Frontend UI Libraries
- **Radix UI**: Comprehensive set of accessible, unstyled React components
- **Tailwind CSS**: Utility-first CSS framework for styling
- **Lucide React**: Modern icon library with consistent design
- **class-variance-authority**: Utility for creating variant-based component styles

## Data Management
- **Drizzle ORM**: TypeScript-first ORM for PostgreSQL
- **TanStack Query**: Powerful data synchronization for React applications
- **React Hook Form**: Performant forms library with minimal re-renders
- **Zod**: TypeScript-first schema validation library

## File Processing
- **xlsx**: Library for reading and writing Excel files
- **File API**: Browser-native file handling for import/export functionality

## Development Tools
- **Vite**: Fast build tool and development server
- **TypeScript**: Static type checking for enhanced developer experience
- **ESBuild**: Fast JavaScript bundler for production builds
- **PostCSS**: CSS processing tool with autoprefixer for browser compatibility

## Deployment Platform
- **Vercel**: Optimized hosting platform with automatic deployments and serverless functions support