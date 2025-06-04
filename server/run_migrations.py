"""Script to run database migrations"""

import os
import sys
import importlib.util
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_migration_module(file_path):
    """Dynamically load a migration module from file path"""
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run_migrations():
    """Run all migration scripts in the migrations directory"""
    migrations_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'migrations')

    if not os.path.exists(migrations_dir):
        logger.error(f"Migrations directory not found: {migrations_dir}")
        return False

    migration_files = [f for f in os.listdir(migrations_dir) if f.endswith('.py')]

    if not migration_files:
        logger.info("No migration files found.")
        return True

    logger.info(f"Found {len(migration_files)} migration files.")

    success = True
    for migration_file in sorted(migration_files):
        file_path = os.path.join(migrations_dir, migration_file)
        logger.info(f"Running migration: {migration_file}")

        try:
            migration_module = load_migration_module(file_path)
            if hasattr(migration_module, 'upgrade'):
                migration_module.upgrade()
                logger.info(f"Successfully applied migration: {migration_file}")
            else:
                logger.warning(f"Migration {migration_file} has no upgrade function.")
        except Exception as e:
            logger.error(f"Error applying migration {migration_file}: {e}")
            success = False

    return success

if __name__ == "__main__":
    logger.info("Starting database migrations...")
    if run_migrations():
        logger.info("All migrations completed successfully.")
        sys.exit(0)
    else:
        logger.error("Some migrations failed.")
        sys.exit(1)
