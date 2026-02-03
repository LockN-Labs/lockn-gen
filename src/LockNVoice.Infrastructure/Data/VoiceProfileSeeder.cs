using System;
using System.Linq;
using LockNVoice.Infrastructure.Data;
using LockNVoice.Domain.Models;

namespace LockNVoice.Infrastructure.Data
{
    public class VoiceProfileSeeder
    {
        public void Seed(VoiceProfileContext context)
        {
            if (!context.VoiceProfiles.Any())
            {
                var profiles = new[]
                {
                    CreateVoiceProfile("Nova", "Warm, friendly female voice"),
                    CreateVoiceProfile("Atlas", "Deep, authoritative male voice"),
                    CreateVoiceProfile("Echo", "Neutral, professional voice"),
                    CreateVoiceProfile("Luna", "Soft, gentle voice")
                };

                context.VoiceProfiles.AddRange(profiles);
                context.SaveChanges();
            }
        }

        private VoiceProfile CreateVoiceProfile(string name, string description)
        {
            // Deterministic GUID based on name hash
            using (var sha1 = System.Security.Cryptography.SHA1.Create())
            {
                var hashBytes = sha1.ComputeHash(System.Text.Encoding.UTF8.GetBytes(name));
                var guidBytes = new byte[16];
                Array.Copy(hashBytes, 0, guidBytes, 0, 16);
                
                return new VoiceProfile
                {
                    Id = new Guid(guidBytes),
                    Name = name,
                    Description = description,
                    ReferenceAudioPath = $"/audio/voice_samples/{name.ToLower()}.wav"
                };
            }
        }
    }
}
