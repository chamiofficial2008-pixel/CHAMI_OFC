import makeWASocket, { useMultiFileAuthState } from '@whiskeysockets/baileys';
import ytDlp from 'yt-dlp-exec';
import express from 'express';
import fs from 'fs';

const app = express();
app.get('/', (req, res) => res.send('Bot running'));
app.listen(8080);

async function startBot() {
    const { state, saveCreds } = await useMultiFileAuthState('auth');
    const sock = makeWASocket({ auth: state });

    sock.ev.on('creds.update', saveCreds);

    sock.ev.on('messages.upsert', async ({ messages }) => {
        const msg = messages[0];
        if (!msg.message || msg.key.fromMe) return;

        const text = msg.message.conversation || msg.message.extendedTextMessage?.text;
        if (!text ||!text.includes('facebook.com')) return;

        await sock.sendMessage(msg.key.remoteJid, { text: 'Video eka download wenawa...⏳' });

        try {
            const result = await ytDlp(text, {
                format: 'best[ext=mp4]',
                output: 'video.mp4',
                noWarnings: true
            });

            await sock.sendMessage(msg.key.remoteJid, {
                video: { url: './video.mp4' },
                caption: 'Me meka'
            });

            fs.unlinkSync('./video.mp4');
        } catch (err) {
            await sock.sendMessage(msg.key.remoteJid, { text: 'Error awa: ' + err.message });
        }
    });

    console.log('Bot ready! QR scan karapan');
}

startBot();
