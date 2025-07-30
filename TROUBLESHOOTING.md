# Troubleshooting Guide

## Common Setup Issues

### 1. Python Dependencies Installation Failures

#### Issue: `torch==2.1.1` not found
**Error**: `ERROR: Could not find a version that satisfies the requirement torch==2.1.1`

**Solution**:
1. The setup script now automatically tries alternative versions
2. If still failing, manually install torch:
   ```bash
   pip install torch>=2.2.0
   ```
3. Or use CPU-only version:
   ```bash
   pip install torch --index-url https://download.pytorch.org/whl/cpu
   ```

#### Issue: Other dependency conflicts
**Solution**:
1. Try the minimal requirements file:
   ```bash
   pip install -r requirements-minimal.txt
   ```
2. Install core dependencies manually:
   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib boto3
   ```

### 2. Database Connection Issues

#### Issue: PostgreSQL connection failed
**Error**: `connection to server at "localhost" (127.0.0.1), port 5432 failed`

**Solutions**:
1. Ensure PostgreSQL is running:
   ```bash
   # Windows
   net start postgresql
   
   # macOS/Linux
   sudo systemctl start postgresql
   ```
2. Check your `.env` file has correct database URL
3. Create database if it doesn't exist:
   ```sql
   CREATE DATABASE content_platform;
   ```

### 3. Frontend Installation Issues

#### Issue: npm install fails
**Solutions**:
1. Clear npm cache:
   ```bash
   npm cache clean --force
   ```
2. Delete node_modules and reinstall:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```
3. Use yarn instead:
   ```bash
   yarn install
   ```

### 4. AWS Configuration Issues

#### Issue: AWS credentials not found
**Error**: `NoCredentialsError: Unable to locate credentials`

**Solutions**:
1. Set environment variables in `.env`:
   ```
   AWS_ACCESS_KEY_ID=your-access-key
   AWS_SECRET_ACCESS_KEY=your-secret-key
   AWS_REGION=us-east-1
   ```
2. Or configure AWS CLI:
   ```bash
   aws configure
   ```

### 5. Port Already in Use

#### Issue: Port 8000 or 3000 already in use
**Solutions**:
1. Find and kill the process:
   ```bash
   # Windows
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   
   # macOS/Linux
   lsof -ti:8000 | xargs kill -9
   ```
2. Use different ports:
   ```bash
   # Backend
   uvicorn backend.main:app --port 8001
   
   # Frontend
   npm start -- --port 3001
   ```

### 6. Docker Issues

#### Issue: Docker containers not starting
**Solutions**:
1. Check Docker is running
2. Check available disk space
3. Restart Docker service
4. Check logs:
   ```bash
   docker-compose logs
   ```

### 7. Memory Issues

#### Issue: Out of memory during model loading
**Solutions**:
1. Use CPU-only models:
   ```python
   # In your code
   torch.set_num_threads(4)  # Limit CPU threads
   ```
2. Reduce batch sizes
3. Use smaller models

### 8. SSL/TLS Issues

#### Issue: SSL certificate errors
**Solutions**:
1. For development, disable SSL verification:
   ```python
   import ssl
   ssl._create_default_https_context = ssl._create_unverified_context
   ```
2. Update certificates:
   ```bash
   pip install --upgrade certifi
   ```

## Getting Help

1. Check the logs in the `logs/` directory
2. Review the README.md for detailed setup instructions
3. Check the API documentation at `http://localhost:8000/docs`
4. Verify all environment variables are set correctly in `.env`

## Environment-Specific Issues

### Windows
- Use PowerShell or Command Prompt as Administrator
- Ensure Python is in PATH
- Use Windows Subsystem for Linux (WSL) for better compatibility

### macOS
- Use Homebrew for package management
- Ensure Xcode Command Line Tools are installed
- Use pyenv for Python version management

### Linux
- Install system dependencies:
  ```bash
  sudo apt-get update
  sudo apt-get install python3-dev build-essential
  ```
- Use virtual environments:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ``` 