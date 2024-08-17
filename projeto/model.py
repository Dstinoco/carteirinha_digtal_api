from projeto import database
from passlib.hash import pbkdf2_sha256



class Users(database.Model):

    __tablename__ = 'aux_api_auth'

    Id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    Username = database.Column(database.String(20), unique=True, nullable=False)
    Password = database.Column(database.String(200), nullable=False)
    Name = database.Column(database.String(60), nullable=False)
    Email = database.Column(database.String(50), unique=True, nullable=False)
    Status = database.Column(database.String(50), unique=False, nullable=False)
    
    
    def __init__(self, Username, Password, Name, Email, Status):
        self.Username = Username
        self.Password = pbkdf2_sha256.hash(Password)
        self.Name = Name
        self.Email = Email
        self.Status = Status
        
    def check_password(self, Password):
        return pbkdf2_sha256.verify(Password, self.Password)    