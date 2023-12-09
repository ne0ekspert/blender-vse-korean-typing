# Add following custom attributes on VSE text strip
# typingAnimation: bool = True
# typingFrames: int = 60 # typing duration of text
# typingText: str = "asdf" # text to type

import bpy
from hangul_utils import split_syllables, join_jamos

# sequence_editor.sequences_all["텍스트"]["typingAnimation"]
scene = bpy.data.scenes['Scene']
vse = scene.sequence_editor

def koreanTypingAnimation(scene):
    animatedStrips = [ v for k, v in vse.sequences_all.items() if v.get('typingAnimation') ]

    for strip in animatedStrips:
        progress = (scene.frame_current - strip.frame_start) / strip['typingFrames']
        if progress < 0:
            continue
        elif progress > 1:
            progress = 1 
        deblock = split_syllables(strip['typingText'])
        deblock_len = int(len(deblock) * progress)
            
        block = join_jamos(deblock[:deblock_len])
        
        strip.text = block
        
if not koreanTypingAnimation.__name__ in [hand.__name__ for hand in bpy.app.handlers.frame_change_pre]:
    bpy.app.handlers.frame_change_pre.append(koreanTypingAnimation)
    
if not koreanTypingAnimation.__name__ in [hand.__name__ for hand in bpy.app.handlers.render_pre]:
    bpy.app.handlers.render_pre.append(koreanTypingAnimation)
