# Ignore all data by default
# Ignore ONLY real data
data/real_backup/

# Allow dummy data
!data/raw/city/*
!data/raw/hospitals/*

# Keep folders
!data/
!data/raw/
!data/raw/city/
!data/raw/hospitals/


# Models
models_tff/
!models_tff/.gitkeep

# Jupyter & Python cache
.ipynb_checkpoints/
__pycache__/
*.pyc

# Virtual envs
.venv/
venv/
env/

# OS files
.DS_Store
Thumbs.db
