projectName = "Dark Genshin Loading Screen"
projectNameShort = "DG-LS"
projectDiscord = "https://discord.gg/7JXXvkufJK"
projectAuthor = "SleepyFish"
projectVersion = "1.0"
projectDescription = "Modify the loading screen of Genshin Impact by checking if the screen is white"
projectCreateDate = "21/09/2024"
projectTitle = projectName + " Version: " + projectVersion + " by " + projectAuthor

# Settings
overlayColor = "#1C1C22"
fontColor = "#FFFFFF"
ignoreColor = "#123456"
tickUpdateNormalTimeMilliseconds = 2
tickUpdateOngoingTimeMilliseconds = 600
renderMeme = True

# Render Text formation
# n: normal
# m: medium
# t: title
# Example Medium and Bold = "m:!Random Text"

renderText = ("t:!" + projectName + " Version: " + projectVersion, "m:by " + projectAuthor, "", "n:"+projectDiscord)