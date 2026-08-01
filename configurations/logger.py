import logging


def get_logger(name:str):
    
    try:
        
        logging.basicConfig(
            level= logging.INFO,
            format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        name = name.join("-logger")
        logger = logging.getLogger(name)
        
        return logger
    
    except ValueError as e:
        print(f"Value error: {e}")
        raise
    
    except Exception as e:
        print(f"Error in {name}: {e}")
        raise