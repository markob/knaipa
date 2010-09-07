from google.appengine.ext import db

class DocumentsQueue(db.Model):
  """Contains only links to documents which should be processed"""
  documents = db.ListProperty(int, default=None)
  
  @staticmethod
  def get_instance():
    """Retrieves the documents queue instance"""
    instance = DocumentsQueue.all().get()
    
    if not instance:
      # create documents queue instance if it does not exist
      instance = DocumentsQueue()
      instance.put()
      
    return instance
