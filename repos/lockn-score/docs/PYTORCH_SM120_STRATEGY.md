# PyTorch sm_120 Strategy for RTX Pro 6000 Blackwell

## 1. Confirm compute capability
- NVIDIA’s official CUDA GPU compute capability list shows **RTX PRO 6000 Blackwell (Workstation Edition)** at **Compute Capability 12.0** (SM 120). This confirms **sm_120** is correct for this GPU family. Source: NVIDIA CUDA GPU Compute Capability list (developer.nvidia.com/cuda/gpus).

## 2. PyTorch CUDA compatibility requirements
- PyTorch wheels are built against specific CUDA toolkits. The official “Previous PyTorch Versions” page shows recent releases shipping wheels for **CUDA 12.6, 12.8, 12.9, and 13.0** (example: PyTorch 2.8/2.9). Source: pytorch.org/get-started/previous-versions.
- Blackwell support starts with **CUDA Toolkit 12.8** across developer tools, libraries, and compilers (NVIDIA). Source: NVIDIA blog on CUDA Toolkit 12.8.
- NVIDIA’s Blackwell Compatibility Guide states **CUDA apps built with CUDA 2.1–12.8 are compatible with Blackwell GPUs if PTX is included**; otherwise, rebuild is required. It also explains that PTX is forward-compatible and can JIT on newer GPUs, but SASS-only binaries without PTX will fail. Source: NVIDIA Blackwell Compatibility Guide.

**Implication:**
- For PyTorch, the CUDA runtime + driver must be **new enough to support Blackwell**, and the PyTorch build must contain **either sm_120 cubins or PTX** so JIT can generate sm_120 at runtime.

## 3. Do we need custom compilation?
**Short answer:**
- **If the installed PyTorch wheel includes PTX** for its highest supported arch, it *should* run on Blackwell via JIT (per NVIDIA’s guide). But **optimal performance and full kernel coverage** usually require **native sm_120 SASS**, which may **not yet be included** in stable PyTorch wheels depending on the release and build configuration.

**Recommendation:**
1. **Try the latest stable PyTorch wheel built for CUDA 12.8+** (or 12.9/13.0). These are officially published on PyTorch’s site.
2. **Verify PTX fallback compatibility**:
   - Set `CUDA_FORCE_PTX_JIT=1` and run a minimal CUDA op (per NVIDIA Blackwell guide). If it runs, the wheel contains PTX and is forward-compatible.
3. **If any kernels fail or performance is poor**, build from source with explicit sm_120:
   - `TORCH_CUDA_ARCH_LIST="12.0"` (or `"12.0+PTX"` for forward-compat)
   - Use **CUDA 12.8+** toolchain (first release with Blackwell support).

## 4. torchvision / torchaudio compatibility
- PyTorch, torchvision, and torchaudio are **version-locked** and should be installed together from the same release series.
- Example from official install page:
  - **PyTorch 2.9.1** pairs with **torchvision 0.24.1** and **torchaudio 2.9.1** (wheels for CUDA 12.6/12.8/13.0). Source: pytorch.org/get-started/previous-versions.

**Action:** For Blackwell, install **matching torchvision/torchaudio** from the **same CUDA wheel channel** (cu128/cu129/cu130) as torch.

## 5. Performance optimizations for Blackwell
**From NVIDIA CUDA 12.8 announcement:**
- CUDA 12.8 is the first release to fully support Blackwell across the toolchain.
- It introduces **Blackwell CUTLASS kernels** and **2nd-gen Transformer Engine** features that improve LLM performance and enable new data types. (Source: NVIDIA CUDA 12.8 blog.)

**Practical PyTorch knobs to consider:**
- **Use CUDA 12.8+ and recent PyTorch** to get newer kernel libraries and arch support.
- **Enable TF32** for matmul on supported ops:
  - `torch.backends.cuda.matmul.allow_tf32 = True`
  - `torch.set_float32_matmul_precision("high")`
- **Use BF16/FP16/FP8 where supported** (for inference workloads such as YOLO/Whisper/ImageBind) to leverage Blackwell Tensor Cores.
- **torch.compile / CUDA Graphs**: The CUDA 12.8 blog highlights enhanced CUDA Graphs; use `torch.compile` or explicit CUDA graphs for stable workloads to reduce launch overhead.
- **Build/enable optimized attention kernels** (FlashAttention, CUTLASS-based kernels) when possible.

## 6. Suggested decision path (for local inference stack)
1. **Install latest stable PyTorch** with CUDA 12.8+ wheels (torch/torchvision/torchaudio matched).
2. **Smoke test** on RTX Pro 6000 Blackwell:
   - `torch.cuda.get_device_capability()` should return `(12, 0)`.
   - Run a simple CUDA op and a small model.
3. **Force PTX JIT** (CUDA_FORCE_PTX_JIT=1) to validate forward compatibility. If failure → rebuild.
4. **If any errors or performance regressions** → **build PyTorch from source** targeting sm_120.

---
## Sources
- NVIDIA CUDA GPU Compute Capability list (shows RTX PRO 6000 Blackwell at CC 12.0): https://developer.nvidia.com/cuda/gpus
- NVIDIA Blackwell Compatibility Guide (PTX forward-compat + rebuild guidance): https://docs.nvidia.com/cuda/blackwell-compatibility-guide/
- NVIDIA CUDA 12.8 Blackwell support announcement: https://developer.nvidia.com/blog/cuda-toolkit-12-8-delivers-nvidia-blackwell-support/
- PyTorch “Previous Versions” (CUDA wheel availability + version matching): https://pytorch.org/get-started/previous-versions/
