from casework.server import app
import os

print "MINT URL2" 
print app.config['MINT_URL']
app.run(host="0.0.0.0", port=int(os.environ['PORT']), debug=True)
