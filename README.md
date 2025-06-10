# Hobby-Lib: AI-Powered Personalized Learning Platform

## Project Overview
Hobby-Lib is an AI-driven personalized learning platform that automatically generates customized study plans based on user interests. The platform leverages Google Gemini AI model to provide structured course content, real-time learning reminders, and intelligent test assessments.

## Core Features

### 1. AI-Driven Course Planning
- Utilizes Google Gemini 2.0 Flash model for personalized learning paths
- Intelligently analyzes learning topics, automatically generating 3-4 learning stages
- Creates 5-10 specific learning sections for each stage
- Supports multiple learning domains, from programming to artistic creation

### 2. Intelligent Content Generation
- Automatically generates detailed course content
- Provides professional yet accessible knowledge explanations
- Includes practical cases and examples
- Uses metaphors and analogies to enhance understanding

### 3. Smart Testing System
- Automatically generates targeted test questions
- Includes multiple-choice and essay questions
- Designs questions based on course key points and difficulties
- Intelligently evaluates learning progress

### 4. Automated Learning Reminders
- Sends course reminders based on user-specified times
- Regularly sends learning tests
- Integrated email notification system

## Technical Features

### AI Model Integration
- Uses LangChain framework for AI interaction management
- Implements Pydantic models for standardized output
- Smart prompt template management
- Structured output parsing

### System Architecture
- FastAPI backend framework
- PostgreSQL database
- Asynchronous task scheduling
- Email notification system

## Project Files Description

1. **main.py**
   - Main application entry point
   - Implements FastAPI routes and endpoints
   - Manages application lifecycle and scheduling
   - Handles lesson registration and automated content delivery

2. **model.py**
   - Core AI model implementation
   - Contains LangChain integration
   - Implements course generation, session content, and test generation
   - Manages AI model interactions and output parsing

3. **mail.py**
   - Email service implementation
   - Handles SMTP configuration and email sending
   - Manages learning reminders and test notifications
   - Implements error handling for email operations

4. **pg.py**
   - PostgreSQL database interface
   - Implements connection pooling
   - Manages lesson data storage and retrieval
   - Handles user progress tracking

5. **testModel.py**
   - Test script for AI model functionality
   - Demonstrates course generation capabilities
   - Tests session content generation
   - Validates test question generation