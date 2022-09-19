from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Personalization, Bcc
from python_http_client import exceptions

SENDGRID_API_KEY = "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"
SENDGRID_SENDER  = "admin@autoave.in"
TEMPLATE_ID = "d-ec1936dc58e34674b047ece126039777"





to_emails = [
    # ('vermasubodhk@gmail.com', 'Suobdh Verma Personal'),
    # ('subodh.verma.min19@iitbhu.ac.in', 'Suobdh Verma IITBHU',),
    # ('suryansh.stomar.min19@iitbhu.ac.in', 'Suryansh Singh Tomar')
    # ('d365labs@gmail.com', 'Jayesh Jaiswal'),
    # ('abhishek.goyal@gmail.com', 'Abhishek Goyal'),
    # ('akhil10s@gmail.com', 'Akhil Gupta'),
    # ('ap@ibulkers.com', 'Alok Pinto'),
    # ('ananda.kallugadde@neobytes.com', 'Ananda kallugadde'),
    # ('aravind.raghavendra1@gmail.com', 'Aravind Raghavendra'),
    # ('archana@adi.vc', 'Archana Priyadarshini'),
    # ('chiragiitb@gmail.com', 'Chirag Gandhi'),
    # ('harishgudi@yahoo.com', 'Harish Gudi'),
    # ('invest@lijoisac.com', 'LIJO ISAC'),
    # ('mekin.m@gmail.com', 'Mekin Maheshwari'),
    # ('midhundandamudi@gmail.com', 'Midhun Dandamudi'),
    # ('faraz697@gmail.com', 'Mohamad Faraz'),
    # ('gupta_naman86@yahoo.in', 'Naman Gupta'),
    # ('ngoenka@gmail.com', 'Nikhil Goenka'),
    # ('nitin@firstprinciples.vc', 'Nitin Sharma'),
    # ('me@pallavn.com', 'Pallav Nadhani'),
    # ('pansare.prashant@gmail.com', 'Prashant Pansare'),
    # ('rajveer.meena@gmail.com', 'Rajveer Meena'),
    # ('rishi@rapido.bike', 'Rishikesh SR'),
    # ('silusreddy@gmail.com', 'Silus Reddy'),
    # ('p13ujwaljs@iima.ac.in', 'Ujwal Sutaria'),
    # ('vaithee.k@gmail.com', 'Vaitheeswaran K'),
    # ('me@varadhja.in', 'Varadh Jain'),
    # ('varun.ags@gmail.com', 'Varun Agarwal'),
    # ('bvishi@gmail.com', 'Viswanadha Raju'),
    # ('rohittmutthoo@gmail.com', 'Rohitt Mutthoo'),
    # ('partner@suprvalue.vc', 'Akshay Bhansali'),
    # ('kunal@cred.club', 'Kunal Shah'),
    # ('parag@inventusindia.com', 'Parag Dhol'),
    # ('suumitgeek24@gmail.com', 'Suumit Shah'),
    # ('tanay@mac.com', 'Tanay Tayal'),
    # ('tejasbaldev@gmail.com', 'Tejas Baldev'),
    # ('thekkekara.ashish@gmail.com', 'Ashish Thekkekara'),
    # ('balasubramaniam.avinash@gmail.com', 'Avinash Balasubramaniam'),
    # ('gaurav@credavenue.com', 'Gaurav Kumar'),
    # ('arunvenk89@gmail.com', 'Arun Venkatachalam'),
    # ('kushgrwl@gmail.com', 'Kush Agarwal'),
    # ('minal@amaraventures.co', 'Minal Desai'),
    # ('animesh8@gmail.com', 'Animesh Pandey'),
    # ('ankit@dineout.co.in', 'Ankit Mehrotra'),
    # ('ashish@posist.com', 'Ashish Tulsian'),
    # ('prakhar@adept.vc', 'Prakhar Agarwal'),
    # ('vedika.work1@gmail.com', 'Vedika Jajodia'),
    # ('hs.381986@gmail.com', 'Harshita'),
    # ('rohitnuwal@gmail.com', 'Rohit Nuwal'),
    # ('prakhar.khanduja@gmail.com', 'Prakhar Khanduja'),
    # ('sayan.work1@gmail.com', 'Sayan Ghosh'),
    # ('sb@delhivery.com', 'Sahil Barua'),
    # ('abhi2point0@gmail.com', 'Abhimanyu Radhakrishnan'),
    # ('ab@amanpreetbajaj.com', 'Amanpreet Singh Bajaj'),
    # ('ankit.pag@gmail.com', 'Ankit Agrawal'),
    # ('ankur@globevestor.com', 'Ankur Shrivastava'),
    # ('KHALID1QAZI@GMAIL.COM', 'Khalid Qazi'),
    # ('lakshya@intellectmedia.in', 'Lakshya Khanna'),
    # ('rahul@kcap.in', 'Rahul Gupta'),
    # ('rhythm.gupta21@gmail.com', 'Rhythm Gupta'),
    # ('rishabhkarwa@gomechanic.in', 'Rishabh Karwa'),
    # ('umeshhora@hotmail.com', 'Umesh Hora'),
    # ('vishaljain.2211@gmail.com', 'Vishal Jain'),
    # ('angel@varunshoor.com', 'Varun Shoor'),
    # ('hiteshchawla@gmail.com', 'Hitesh Chawla'),
    # ('vaibhav.s28@gmail.com', 'Vaibhav Singhal'),
    # ('dhawalshah18@gmail.com', 'Dhawal Shah'),
    # ('mayank@supersourcing.com', 'Mayank Pratap Singh'),
    # ('talash@indusnet.co.in', 'Abhishek Rungta'),
    # ('ferosmd@gmail.com', 'Feroz Mohammed'),
    # ('aacash.kumar@gmail.com', 'Aakash Kumar'),
    # ('aakrit.vaish@gmail.com', 'Aakrit Vaish'),
    # ('abhishek@luminaire.capital', 'Abhishek Nag'),
    # ('aj.goel@creditwisecapital.com', 'AJ Goel'),
    # ('jpakhil@gmail.com', 'Akhil Jayaprakash'),
    # ('mittal.akshay@firstcoffee.in', 'Akshay Mittal'),
    # ('alok@rodinhood.com', 'Alok Kejriwal'),
    # ('Ambuj.j@gmail.com', 'Ambuj Jhunjhunwala'),
    # ('prospects@artha.vc', 'Anirudh A Damani'),
    # ('arjunbvaidya@gmail.com', 'Arjun Vaidya'),
    # ('dave.ashish@miraeasset.com', 'Ashish Dave'),
    # ('ashishpdoshi@gmail.com', 'Ashish Doshi'),
    # ('bharatibalakrishnan+angel@gmail.com', 'Bharati Balakrishnan'),
    # ('dhvanilsheth7@gmail.com', 'Dhvanil Sheth'),
    # ('digjay@gmail.com', 'Digjay Patel'),
    # ('farokh@theobroma.in', 'Farokh Messman'),
    # ('gshewakr@gmail.com', 'Gautam Shewakramani'),
    # ('govind.s@meridian.biz', 'Govind Shorewala'),
    # ('harsh88.shah@gmail.com', 'Harsh Shah'),
    # ('hvbhandari@mgbadvisors.com', 'Harsh vardhan Bhandari'),
    # ('jitengupta@gmail.com', 'Jitender Gupta'),
    # ('aacash.kumar@gmail.com', 'Kumar Aakash'),
    # ('miten.sampat@gmail.com', 'Miten Sampat'),
    # ('neeraj@texport.com', 'Neeraj Goenka'),
    # ('nitesh@threeblindmice.in', 'Nitesh Kripalani'),
    # ('pj@beingpractical.com', 'pj'),
    # ('prakashdeep.m@gmail.com', 'Prakash Deep Maheshwari'),
    # ('pbiswal@marwah.in', 'Pranav Marwah'),
    # ('romildwivedi21@gmail.com', 'Romil Dwivedi'),
    # ('shalin@core91.vc', 'Shalin Shah'),
    # ('bhambri3@gmail.com', 'Sorab Bhambri'),
    # ('contact@stellarisvp.com', 'Stellaris VP'),
    # ('plans@nexusvp.com', 'Nexus VP'),
    # ('karnavatvaibhav@gmail.com', 'Vaibhav Karnavat'),
    # ('viveklath@gmail.com', 'Vivek Lath'),
    # ('asheth99@gmail.com', 'Arpan Sheth'),
    # ('abhinavgrover86@gmail.com', 'Abhinav Grover'),
    # ('amit.lakhotia@gmail.com', 'Amit lakhotia'),
    # ('apurva.chamaria@gmail.com', 'Apurva Chamaria'),
    # ('koladiya@gmail.com', 'Bhavik Koladiya'), 
    # ('kashish@angel.co', 'Kashish Sharma'),
    # ('kk@advantedge.vc', 'Kunal Khattar'),
    # ('mv@vun.co.in', 'Manish Vij'),
    # ('nks@semcoindia.com', 'Neeraj Kumar Singal'),
    # ('RenuSatti@Gmail.com', 'Renu Satti'),
    # ('sanchit@sanchitart.in', 'Sanchit Joshan'),
    # ('shankarnath1973@gmail.com', 'Shankar Nath'),
    # ('u@iseed.vc', 'Utsav Somani'),
    # ('vss@Paytm.com', 'Vijay Shekhar Sharma'),
    # ('me@pjain.me', 'Pankaj Jain'),
    # ('abhishekmgupta@gmail.com', 'Ahbishek Mitra Gupta'),
    # ('infogaufire@gmail.com', 'Gaurav Sharma'),
    # ('pankaj@hellotravel.com', 'pankaj agarwal'),
    # ('sahil@shl.vc', 'Sahil Lavingia'),
    # ('singh.parminder02@gmail.com', 'Parminder Singh'),
    # ('kuldeepseoul@gmail.com', 'Kuldeep Mamgain'),
    # ('kkmehra@gmail.com', 'Krishna Mehra'),
    # ('jagmal@gmail.com', 'Jagmal Singh'),
    # ('pvaranjani@stripe.com', 'Piyush Varanjani'),
    # ('sumesh@saiam.com.sg', 'Sumesh Menon'),
    # ('k.kapoor@gmail.com', 'Ketan Kapoor'),
    # ('chandanmiskin@outlook.com', 'Chandan Miskin'),
    # ('sameer.j.shah@hotmail.com', 'Sameer Shah'),
    # ('kpalania@gmail.com', 'Kumaranand Palaniappan'),
    
    ('pitch@capixal.in', 'Capixal'),
    ('esha@joinef.com', 'Esha Tiwary'),
    # ('reachus@turbostart.co', 'Turbo Start'),
    ('hello@upsparks.vc', 'Up Sparks'),
    ('ray.newal@techstars.com', 'Ray Newal'),
    ('', ''),
    ('', ''),
    ('', ''),
    ('', ''),
    ('', ''),
    ('', ''),
    ('', ''),
    ('', ''),
    ('', ''),
    ('', ''),
    ('', ''),
    ('', ''),
    ('', ''),
    ('', ''),
    ('', ''),
]

# for email, name in to_emails:
#     print((email.strip(), name.strip()))

SUBJECT = "Seeking investment - Aggregator for Car Care Services"

def send_email():
    sendgrid_client = SendGridAPIClient(SENDGRID_API_KEY)
        
    message = Mail(
        from_email= (SENDGRID_SENDER, 'Autoave Private Limited'),
        to_emails=to_emails,
        is_multiple=True
    )
    
    message.template_id = TEMPLATE_ID
    
    # print(message.get())
    
    try:
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except exceptions.BadRequestsError as e:
        print(e.body)
        print(e.body)
        print(e)
        exit()


send_email()