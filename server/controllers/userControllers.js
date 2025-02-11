const users = require("../models/userSchema");
const userotp = require("../models/userOtp");
const nodemailer = require("nodemailer");
const twilio=require('twilio');


// email config
const tarnsporter = nodemailer.createTransport({
    service: "gmail",
    auth: {
        user: "manvitha898@gmail.com",
        pass: "sxxb pvxa lbhi qjda"
    }
})

const accountSid="ACb978d2807d632cfc5193ad11fc81a681";
const authToken="86e4d258d7a5a68bcce16cd6b390e43f";
const client=twilio(accountSid,authToken);



exports.userregister = async (req, res) => {
    const { fname, email, password ,phone} = req.body;

    if (!fname || !email || !password || !phone) {
        res.status(400).json({ error: "Please Enter All Input Data" })
    }

    try {
        const presuer = await users.findOne({ email: email });

        if (presuer) {
            res.status(400).json({ error: "This User Allready exist in our db" })
        } else {
            const userregister = new users({
                fname, email, password,phone
            });

            // here password hasing

            const storeData = await userregister.save();
            res.status(200).json(storeData);
        }
    } catch (error) {
        res.status(400).json({ error: "Invalid Details", error })
    }

};

// user send otp
exports.userOtpSend = async (req, res) => {
    const { email,password } = req.body;
    const user=await users.findOne({email})
    //console.log(user.phone)
    if (!email) {
        res.status(400).json({ error: "Please Enter Your Email" })
    }
    if(!password){
        res.status(400).json({ error: "Please Enter Your Password" })
    }
    else{
        const cpass=await users.findOne({email:email});
        if(!cpass){
            res.status(400).json({ error: "invalid password" })
        }
    }
    try {
        const presuer = await users.findOne({ email: email });

        if (presuer) {
            const OTP = Math.floor(100000 + Math.random() * 900000);

            const existEmail = await userotp.findOne({ email: email });


            if (existEmail) {
                const updateData = await userotp.findByIdAndUpdate({ _id: existEmail._id }, {
                    otp: OTP
                }, { new: true }
                );
                await updateData.save();

                const mailOptions = {
                    from: "manvitha898@gmail.com",
                    to: email,
                    subject: "Sending Eamil For Otp Validation",
                    text: `OTP:- ${OTP}`
                }
                tarnsporter.sendMail(mailOptions, (error, info) => {
                    if (error) {
                        console.log("error", error);
                        res.status(400).json({ error: "email not send" })
                    } else {
                        console.log("Email sent", info.response);
                        res.status(200).json({ message: "Email sent Successfully" })
                    }
                })
                await client.messages.create({
                    body: `YOUR OTP IS: ${OTP}`,
                    to: `+91${8919131081}`,
                    from: '+15745984489',
                });
        

            } else {

                const saveOtpData = new userotp({
                    email, otp: OTP
                });

                await saveOtpData.save();
                const mailOptions = {
                    from: "manvitha898@gmail.com",
                    to: email,
                    subject: "Sending Eamil For Otp Validation",
                    text:`OTP:- ${OTP}`
                }

                tarnsporter.sendMail(mailOptions, (error, info) => {
                    if (error) {
                        console.log("error", error);
                        res.status(400).json({ error: "email not send" })
                    } else {
                        console.log("Email sent", info.response);
                        res.status(200).json({ message: "Email sent Successfully" })
                    }
                })
            }
        } else {
            res.status(400).json({ error: "This User Not Exist In our Db" })
        }
    } catch (error) {
        res.status(400).json({ error: "Invalid Details", error })
    }
};


exports.userLogin = async(req,res)=>{
    const {email,otp} = req.body;
    if(!otp || !email){
        res.status(400).json({ error: "Please Enter Your OTP and email" })
    }

    try {
        const otpverification = await userotp.findOne({email:email});

        if(otpverification.otp === otp){
            const preuser = await users.findOne({email:email});

            // token generate
            const token = await preuser.generateAuthtoken();
           res.status(200).json({message:"User Login Succesfully Done",userToken:token});

        }else{
            res.status(400).json({error:"Invalid Otp"})
        }
    } catch (error) {
        res.status(400).json({ error: "Invalid Details", error })
    }
}