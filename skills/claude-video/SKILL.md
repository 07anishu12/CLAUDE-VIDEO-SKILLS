---
name: claude-video
description: "Directs AI video editing and production across music videos, lyric videos, reels, animation, explainers, podcasts, footage edits, motion effects, and visual looks. Use when the user asks to make, edit, style, or render a video."
---

# Claude Video

Act as the user's video production director. Understand the intended deliverable, choose the closest specialist command, inspect supplied media, build an editing plan, render a preview, and produce a real validated MP4 when the local engine and input assets support the requested result.

## Route the request

1. Identify the deliverable: song or lyric video, animated story, podcast/talking head, short reel, long-video clip, explainer, news report, cinematic montage, effect, look, or custom edit.
2. Select the best matching specialist from the directory below. Match the user's requested visual treatment and source purpose; do not apply all skills or replace a specific style with a generic edit.
3. If the selected specialist is installed and the host supports invocation, ask the user to invoke its command if no direct chaining mechanism exists. Otherwise read and follow that specialist's workflow in this session. Never claim a skill was invoked when it was not.
4. For multiple compatible treatments, combine only the non-conflicting steps (for example, podcast pacing plus comic graphics). State the chosen treatment briefly.
5. If no specialist fits, apply the common inspection, planning, preview, render, and validation process below.

### Fast routes

- Hindi lyrics / Hindi song text: /hindi-lyric-video. Preserve Devanagari when supplied.
- Madhubani story: /madhubani-kahani.
- Podcast reel with clean cuts and punch-ins: /podcast-reel-edit.
- Comic treatment on a podcast: /podcast-comic.
- Anime fight: /anime-fight.
- 3D explainer: /3d-explainer. Check for Blender and a render-capable setup; this FFmpeg engine does not create 3D scenes.
- News-style explainer: /news-report.
- Watercolor map journey: /watercolor-map.
- Music-led cut timing: /beat-transition-edit. Use measured BPM/beat estimates only when the optional analyzer is installed.
- Talking-head captions: /talking-head-edit.
- Short from long-form video: /youtube-clips.

## Production process

1. Locate and inspect user-provided clips, audio, images, lyrics, transcripts, scripts, and references. Never overwrite source media. Ask only for essential missing material.
2. For a song, inspect duration/streams and run audio analysis. BPM is an estimate; do not treat it as exact. Never infer lyrics from music as ground truth. Use supplied/corrected lyrics and actual alignment data for word timing; if alignment is unavailable, ask for timings or use clearly labeled line-level approximations.
3. For a supplied reference, describe observable shot order, pacing, graphic treatment, aspect ratio, and transitions. Do not promise frame-perfect reconstruction.
4. Produce a concise storyboard/timeline specifying shot lengths, focal content, transitions, text, audio, output ratio, and known tool limits.
5. Discover the engine in this order: environment variable VIDEO_SKILLS_ENGINE pointing to video.py; repository engine/video.py; installed project .claude-video/engine/video.py; installed user engine under the user's home .claude-video/engine/video.py; or a plugin-bundled engine folder. Check --help and dependencies before use.
6. Render a low-resolution proxy using the same timeline (for example 360x640 or 640x360 at 12 fps), then create a contact sheet. Show the preview. Ask approval when style, shot selection, or substantial edits are involved; trivial requested trims do not need an extra approval round.
7. Render the final approved MP4 at vertical 1080x1920 for reels or landscape 1920x1080 for YouTube unless requested otherwise. Preserve audio by default and ask before replacing existing outputs.
8. Validate video stream, duration, dimensions, audio/subtitle tracks, and file size with the engine. Return the exact output path and any unavailable feature.

## What the local engine does

The engine edits user-provided video, image, and audio material with FFmpeg: metadata inspection, trims, multiple-clip concatenation, crop/resize, speed, zoom crop, simple color controls, fades, supported cross-transitions, SRT subtitle tracks, contact sheets, and MP4 validation. It does not synthesize footage, characters, 3D scenes, music, or accurate song lyrics. Use a separate media-generation or transcription model only when it is actually available and authorized.

## Specialist command directory

All 80 individual command names and purposes:

| Command | Category | Best fit |
|---|---|---|
| /3d-explainer | Animated videos | A 3D animated news explainer built in Blender, like the Professor of Claude ISRO and Cyclone Arnab reels: Claude builds every 3D shot in code (rockets on launch pads, a 3D India map with pins, a storm spiralling over the sea, Earth from space), cuts the camera on your words and pops the numbers in as you say them. |
| /aarti-video | Animated videos | A devotional aarti video full of fire and light, like the Shiv aarti: glowing diyas, flames, a damru rhythm and the aarti lines in Devanagari. |
| /anime-fight | Animated videos | An anime fight gag in the one-punch style: a sleepy, unbothered hero ends a giant monster with a single punch, then turns the same punch on something relatable, like Monday morning. |
| /anime-reel | Animated videos | An anime-style episode with original characters drawn in code and lip-synced to your voice lines, like the Zero Se Freelance series. |
| /baba-pusho | Animated videos | A Puneet Superstar “Baba Pusho” clip as a cartoon class, like Ye likho ye milega Part 8: Pusho preaches from his desk under a big Om, his fixed class of students reacts, and every Hindi line gets a caption plus a scene of its own. |
| /bairan-style | Animated videos | A romantic lyric video like the Bairan reel: watercolour-painted characters cut out like paper stickers, polaroids, a sunflower and a beating heart popping in, every move fast in and slowly settling. |
| /beat-transition-edit | Animated videos | The trending beat edit from the How to do this with Claude series (Ep 1): your dance or twirl video in smooth slow motion, cutting to your photos on every music hit with a quick zoom-blur dissolve and a warm film grade, copied from any reference reel. |
| /blueprint-explainer | Animated videos | A long YouTube explainer drawn like an engineering blueprint, like the Piramal Finance loan video: a blue grid sheet, white line drawings, and numbers that calculate live as you talk. |
| /comic-reel | Animated videos | A famous movie scene retold as a comic book, like the Drishyam 3 reel: halftone panels, speed lines, BOOM bursts and speech bubbles for every line of dialogue. |
| /crayon-carousel | Animated videos | The trending crayon carousel from How to do this with Claude (Ep 3): every slide puts a crayon drawing of your photo on top, labelled “One day”, over the real photo labelled “Day one”, ready to post as an Instagram carousel. |
| /flicker-edit | Animated videos | The viral flicker edit from How to do this with Claude (Ep 6): two shots from the same tripod spot, one with the model and one of the empty beach, cut against each other about 8 times a second on the beat, so the model appears and vanishes into the sea, with a small zoom to her face every time she comes back. |
| /glass-to-neon-lyrics | Animated videos | An emotional 16:9 lyric video that keeps changing mood with the song, like the Arz Kiya Hai (Anuv Jain × Lost Stories) video: a red glass Apple-Music-style lyrics card over a wall of giant red words that cracks and shatters, then full-screen clips with the lyrics standing in the empty space (a starry red field with twinkling and shooting stars, a sunny hill, a man against the clouds), a key line cut out as giant letters with fire burning inside them, and a pink neon ending where lyrics fall in, splash and reflect in water while it rains. |
| /glow-lyrics | Animated videos | A dreamy lyric video like MITRAZ's Khwahish from Ye likho ye milega Part 7: flat vector scenes at purple dusk, silhouettes that tell the story (a boy alone on a bench, the girl he misses glowing inside a golden birdcage), soft bloom on every light, and the lyric line glowing in word by word. |
| /hindi-lyric-video | Animated videos | A calm Hindi lyric video like Banjaare's “Barsaat”: Devanagari lines write on over old paper while rain falls and footprints walk across the page with the song. |
| /ink-line-lyrics | Animated videos | A fast lyric video drawn as ONE glowing ink line that never breaks, like the Main Aur Tu reel: the line morphs into a new drawing on every key word, with the camera punching on every kick. |
| /katha-video | Animated videos | A pravachan clip turned into an animated story: the characters act out the kahani, the speaker talks from a lip-synced corner badge, and Hindi captions follow every word. |
| /kids-story | Animated videos | A bright 60-second kids story like Pyaasi Chidiya: soft rounded characters, a sunny world, Hindi speech bubbles and a little reacting companion in the corner. |
| /kinetic-lyrics | Animated videos | Big kinetic typography for an English song, like Justin Bieber's “Let Me Love You”: every word punches in on the beat in chunky letters on black, with paint splats and confetti. |
| /latent-comic | Animated videos | An India's Got Latent clip retold as a 9:16 comic book, like the MC Stan episode reels: Samay Raina and the judges at the show's desk on top, a close-up of whoever is talking below with a gag for every line, halftone dots, bursts and speech-bubble captions. |
| /latent-reel | Animated videos | A roast-show clip turned into a cartoon, like Samay Raina's India's Got Latent: the guest at the mic on the left, the host reacting on the right, the show's stage behind them. |
| /lyric-video | Animated videos | A hand-drawn crayon lyric video on a dark chalkboard: every word writes on as it's sung, and each line gets its own little drawing. |
| /madhubani-kahani | Animated videos | A Panchatantra-style story told as a living Madhubani painting: double black outlines, patterned fills, fish-scale water and a red-yellow folk border. |
| /madira-peekar-soo-gaye | Animated videos | A famous movie dialogue turned into a comic-book scene, like the Drishyam 3 “madira peekar so gaye” clip from Ye likho ye milega Part 8: one character delivers the line in a speech bubble word by word, then the other explodes in close-up with speed lines and a colour flash. |
| /maut-ke-bare-mai-sochte-ho | Animated videos | A podcast moment retold as a comic page, like the Ranveer × Honey Singh “manzil kya hai? … Death.” clip from Ye likho ye milega Part 8: the host's big question in a speech bubble, a long silent beat, then DEATH. slams in on black with a skull and the guest gulps in an inset panel. |
| /minimal-lyrics | Animated videos | A quiet, minimal lyric video like Bayaan's Safar from Ye likho ye milega Part 7: a flat horizon, a lone silhouette walking, wind drawn as sweeping streak lines, and a sky whose colour follows the mood of each line, with one small serif lyric line at the bottom. |
| /mirzapur-video | Animated videos | A web-series dialogue turned into a comic meme, like the Kaalin Bhaiya “chai piyoge?” reel: a bold comic portrait of the don, halftone backgrounds that change on every beat, and a POV caption. |
| /neon-lyrics | Animated videos | A synthwave rap lyric video like KR$NA's “I Guess”: a neon grid, a big retro sun, a cartoon of the rapper in a varsity jacket and glowing Hindi lyrics. |
| /news-report | Animated videos | A Hinglish tech-news report in Fireship style: flat dark background, screenshot cards with red boxes and highlights, memes, and a hard cut every two seconds, with you as the anchor. |
| /night-glow-lyrics | Animated videos | A 16:9 lyric video that makes people feel the song, like the Dooron Dooron (Paresh Pahuja ft. Harleen Sethi) video: one night-blue look with glowing white light, emotional clips that follow the story of each line, an Instagram post that dives into the title, and lyrics that change style with the music (small tracked caps + one huge serif word for the key lines, simple bottom lines in between), ending with the last line turning to light. |
| /painted-beat-edit | Animated videos | A viral footage edit remade with no footage at all, like the Shiv aarti reel from How to do this with Claude (Ep 2): Claude paints the images in code in an acrylic mural style and cuts between them on every half-beat with a slow zoom. |
| /paper-cutout | Animated videos | A paper-cutout music video like Jaadoo: hand-cut paper characters, floating islands and lyric tags that pop on their words, moving in 15 fps stop-motion. |
| /party-lyrics | Animated videos | A loud party-anthem lyric video, like Honey Singh's Casa Tupka: gold and gem 3D lettering, red curtains and lavender smoke, confetti on every beat, and a cartoon of the singer in their signature look. |
| /personal-explainer | Animated videos | An explainer in your own voice, like “How will the Tesla fly?”: real footage with credit, clean diagrams that build step by step, numbers that pop, and you as the narrator. |
| /pink-spotify-clip-lyrics | Animated videos | A poetic 16:9 lyric video like the Alfaaz (Hamza Malik × Zain Zohaib) video: a tilted pink Spotify lyrics card, then motion graphics that follow the meaning of each line (a rose that draws itself, letters cut out of the clip, a cinema letterbox, a dotted footstep path with the words along it, and a split screen for the last line), with my emotional clips playing softly behind the lyrics so both the video and the words stay readable. |
| /podcast-cartoon | Animated videos | A famous podcast moment turned into a gag: the podcast clip plays, then an original cheeky cartoon kid pops in as a sticker and asks the big question, and you react, like the “maut ke baare mein sochte ho?” reel. |
| /podcast-comic | Animated videos | A podcast clip retold as a 9:16 comic book, like the Raj Shamani “ladke ko kab jaanoge” reel: the guest drawn in the studio below (bookshelf, Break the Cage poster, mic), and a new comic panel slams in on top for every point he makes, with a burst word and Hindi speech-bubble captions. |
| /podcast-explainer | Animated videos | A podcast clip turned into an animated explainer, like the Raj Shamani “Two Winners” video: simple stick-figure metaphors for every idea, bold kinetic captions, and the host drawn as a cartoon in a live corner window. |
| /pusho-reel | Animated videos | A Puneet Superstar “Baba Pusho” cartoon reel with the full class: Baba Pusho teaching, his students reacting, Hindi captions on every word, a new scene for every line. |
| /rap-video | Animated videos | A full-energy cartoon rap video like Boom Shaka: the rapper drawn as a bold cartoon, BOOM bursts, speed lines and lyrics that slam in on every beat. |
| /red-rap-lyrics | Animated videos | A fast rap lyric video in one red grade, like the Hola Amigo (KR$NA ft. Seedhe Maut) video: a red glass lyrics card that peels in like a page over a tilted wall of lyric words, then neon words standing on a rainy street with ripple reflections, then the rapper's photo turned into a monochrome particle portrait with stacked italic lyrics lighting up word by word, and a 3D tower of words where the camera eases to every new word, ending on a DAMN! slam. |
| /scribble-edit | Animated videos | Your own clip covered in live marker doodles, like the Justin Bieber “Where Are Ü Now” video from How to do this with Claude (Ep 5): the wall behind you fills with hand-drawn stars, rockets, cats and lightning, crowns and shades stick to your face as you move, a neon line traces your body, and the whole look changes on every beat. |
| /shadow-puppet | Animated videos | A kids story told like tholu bommalata shadow puppets: black cut-out characters with pin joints moving against a glowing orange screen. |
| /sketch-doodle-edit | Animated videos | One photo turned into the trending sketch doodle edit from How to do this with Claude (Ep 4): the people flicker between the real photo and a pencil sketch on the beat, white wind lines swoosh across the sky, a scribble outline draws around them and a handwritten line writes itself in. |
| /sketch-music-video | Animated videos | A pencil-sketch lyric video like Anuv Jain's “Inaam”: soft graphite drawings of the song's story fill the page while the lyrics are handwritten next to them, line by line. |
| /sketch-to-motion | Animated videos | Your rough paper sketches turned into a polished app-promo animation: the sketch stays on the left, the finished motion graphic plays next to it, like the Kulhad chai reel. |
| /spotify-particle-lyrics | Animated videos | A 16:9 lyric video in four looks, like the Kalyani (ARJN × KDS × Fifty4 × Ronn ft. Shreya Ghoshal) video: a tilted Spotify lyrics card where every sung word lights up with glowing sparks, then the artists' photo turned into a monochrome particle portrait that morphs into a second photo while red-and-white lyrics pop on the right and dance on the beat, then gold motion-graphic lyrics with fast blur word changes for the singer's part, and a black-and-white rain-on-glass music player to end. |
| /street-interview | Animated videos | A funny street interview turned into a cartoon, like the bad day interview: the interviewee drawn as a flat cartoon, night-street background and big caption words on the punchlines. |
| /talking-head-edit | Animated videos | Your raw clip, fully edited: captions on every word, the screen splits into two windows to show what you're talking about, and demo videos play full screen. Your face is never re-coloured. |
| /titan-anime | Animated videos | An anime episode set in an Attack on Titan-style world: giant walls, green capes, horses, flags and titans, with your own original characters telling the story. |
| /watercolor-lyrics | Animated videos | A soft lyric video like Ashu Shukla's Phir Se Shuru from Ye likho ye milega Part 7: the camera pans right across warm paper while autumn watercolour scenes of one couple draw themselves in (ink lines first, then the wash blooms), leaves fall, and the lyric lines write on word by word. |
| /watercolor-map | Animated videos | A painted watercolor world map: a pin drops on the start city, a plane flies the real great-circle route, and the destination washes in with colour. |
| /woof-woof | Animated videos | A streamer's live moment as a cartoon, like the IShowSpeed “woof woof” clip from Ye likho ye milega Part 8: he stares into the camera, then barks on every beat while WOOF! bursts fly, the live chat floods with woofs and the viewer count shoots up. |
| /business-short-form-reels | Reel formats | A reel for business topics, with docs, decks and screen recordings as B-roll. |
| /depth-ui-reel | Reel formats | Floating app interfaces that sit behind my head, with my body cut out in front of them. |
| /educational-youtube-editor | Reel formats | Turn a long lesson recording into a clean, chaptered YouTube edit. |
| /personal-broll-library | Reel formats | Search my own B-roll folder in plain English ("me walking at night") and return the best matching clips. |
| /personal-short-form-reels | Reel formats | A fast personal reel with my own B-roll and word-by-word captions. |
| /ranking-format | Reel formats | A tier-list reel: items ranked one by one, S to F. |
| /youtube-clips | Reel formats | Find the best moments in a long YouTube video and turn each into a vertical clip. |
| /glass-stat-card | Motion effects | A frosted-glass card with a number that counts up live. |
| /led-matrix-text | Motion effects | Big dot-matrix words, one per beat, like a stadium screen. |
| /match-cut | Motion effects | The same word on a new page, landing in exactly the same spot on screen. |
| /particle-chart | Motion effects | Particles pour down and pile up into a bar chart. |
| /particle-text | Motion effects | Words built out of falling dots that assemble on the beat. |
| /price-tag-zoom | Motion effects | A slow push-in on a product with a floating price tag. |
| /shutter-stack | Motion effects | Photo cards that drop in on a camera flash, stacking up. |
| /dark-red-timeline-motion-graphics | Edit styles | A dark red grade, a blinking REC tag and an animated timeline. |
| /hindi-pastel-reel-edit | Edit styles | A soft pastel set with one giant word behind my head. |
| /instagram-ui-hinglish | Edit styles | Instagram profile grids behind me, with tick-mark chips for each point. |
| /iphone-style-by-aansh | Edit styles | Frosted iOS widgets and notifications floating over my footage. |
| /kinetic-talking-head-edit | Edit styles | A cream panel with green highlight typography that moves with my words. |
| /podcast-reel-edit | Edit styles | Tight cuts, a clean headline and punch-ins, podcast-clip style. |
| /red-kinetic-collage-edit | Edit styles | Black-and-white footage with one glowing red word and collage-style type. |
| /breaking-news | Looks | A TV-news lower third, a scrolling ticker and a channel bug. |
| /cinema-scope | Looks | 2.39:1 film bars, film grain and a title card. |
| /comic-halftone | Looks | Halftone dots, a comic panel border, speech bubbles and POW words. |
| /magazine-cover | Looks | A magazine masthead behind my head, with cover lines around me. |
| /neon-outline | Looks | A glowing neon outline around me, with neon words. |
| /rgb-glitch-live | Looks | Split colour channels, torn slices and a live news chyron. |
| /triptych-timecode | Looks | Three clips side by side, each with its own live timecode. |

## Missing capability handling

If the user asks for generated animation, image generation, forced lyric alignment, or 3D and no suitable model/tool is available, explain the missing component and offer an edit using provided assets. Do not label a still-image montage as generated animation. If the engine or codec fails, preserve all sources, report the actual error, and do not claim a final render.
