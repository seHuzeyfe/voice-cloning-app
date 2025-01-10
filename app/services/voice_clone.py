import subprocess
from pathlib import Path
from fastapi import HTTPException
import os

class VoiceCloneService:
    def __init__(self, use_cuda: bool = False):
        self.checkpoint_dir = Path("checkpoints/fish-speech-1.5")
        self.vqgan_path = self.checkpoint_dir / "firefly-gan-vq-fsq-8x1024-21hz-generator.pth"
        self.use_cuda = use_cuda

        # Set environment variable for CUDA availability
        if not use_cuda:
            os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Disable CUDA

    async def clone_voice(
            self,
            input_audio_path: Path,
            target_text: str,
            reference_text: str,

    ) -> Path:
        """
        Clone voice using the inference pipeline by fish-speech repository.
        Following the three steps from inference.md:
        1. Generate prompt from voice (VQGAN encode)
        2. Generate semantic tokens from text (LLaMA)
        3. Generate final audio (VQGAN decode)
        """
        try:
            # Step 1: Generate prompt from voice using VQGAN
            subprocess.run([
                "python", "tools/vqgan/inference.py",
                "-i", str(input_audio_path),
                "--checkpoint-path", str(self.vqgan_path),
                "--device", "cpu"
            ], check=True)

            # Step 2: Generate semantic tokens from text using LLaMA
            subprocess.run([
                "python", "tools/llma/generate.py",
                "--text", target_text,
                "--prompt-text", reference_text,
                "--prompt-tokens", "fake.npy",
                "--checkpoint-path", str(self.checkpoint_dir),
                "--num-samples","1",
                "--device", "cpu"
                #"--compile" # For faster inference

            ], check=True)

            # Step 3: Generate final audio using VQGAN decoder
            subprocess.run([
                "python", "tools/vqgan/inference.py",
                "-i", "codes_0.npy",
                "--checkpoint-path", str(self.vqgan_path),
                "--device", "cpu"
            ],check=True)

            # The final output will be 'fake.wav'
            output_path = Path("fake.wav")
            if not output_path.exists():
                raise RuntimeError("Output audio file was not generated.")
            return output_path
        
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Voice cloning process failed: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"An error occured: {str(e)}")