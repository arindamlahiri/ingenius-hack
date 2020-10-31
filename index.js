require('dotenv').config()
const spawn = require("child_process").spawn;
const { Client } = require('discord.js')
const client = new Client()
const mongoClient = require('mongodb').MongoClient
const { bot_token,db_url } = process.env
let dbo

client.once('ready', () => {
    console.log('Bot online!')
    mongoClient.connect(db_url,{ useUnifiedTopology:true }, (err,db) => {
        if(err) return console.error(err)

        console.log(`database connected`)
        dbo = db.db('discord-bot')
    })
});

client.on('message', async(message) => {
    if(message.author.bot || message.type !== 'DEFAULT') return;

    let text = message.cleanContent
    let { id } = message.author
    console.log(text)
    const process = spawn('python',["app1.py",text]);
    let output = []

    process.stdout.on('data', (data) => { 
        output.push(data.toString())
    })

    process.stdout.on('close', async(code) => {
        output = output[output.length-1]
        console.log(JSON.stringify(output))
        if(output === 'offensive\r\n') {
            let user = await findUserById(id)
            if(!user) {
                let data = {
                    discordId:id,
                    offences:1
                }
                await insertUser(data)
                message.reply("This is your first warning for an inappropriate message.")
            } else if(user.offences == 1) {
                await updateOffences(id)
                message.reply("This is your second warning. You will be kicked if such messages are continued")
            } else if(user.offences == 2){
                const member = message.guild.members.cache.get(id)
                await kickUser(member,message)
                await deleteUser(id)
            }
        }
    })
        
})

async function findUserById(id){
    try {
        return dbo.collection('users').findOne({ discordId:id })
    } catch(err){
        return console.error(err.message)
    }
}

async function insertUser(data){
    try {
        return dbo.collection('users').insertOne(data)
    } catch (err) {
        return console.error(err.message)
    }
}

async function updateOffences(id){
    try {
        return dbo.collection('users').updateOne({ discordId:id }, {$set:{offences:2}})
    } catch (err) {
        return console.error(err.message)
    }
}

async function deleteUser(id){
    try {
        return dbo.collection('users').deleteOne({ discordId:id })
    } catch(err){
        return console.error(err.message)
    }
}

async function kickUser(member,msg){
    if(member){
        try{
            await member.kick()
            msg.channel.send(`${member} was kicked from the server.`)
        } catch(e){
            console.error(e.message)
            msg.channel.send(`Could not kick ${member} :(`)
        }
    } else {
        return console.log('member not found')
    }
}

client.login(bot_token)