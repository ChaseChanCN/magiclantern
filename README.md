# 魔灯 Magic Lantern — 中文汉化版

[English Version](#english-version) | [中文版](#中文版)

---

## 中文版

Magic Lantern（魔灯，简称 ML）是一个为佳能数码相机提供额外功能的开源软件增强平台。它以 GPL 许可证发布，在佳能官方固件之上独立运行，**不会替换或修改原厂固件**。

本项目是 Magic Lantern 的**中文（简体）汉化版**，由 [Chase Chan](https://github.com/ChaseChanCN) 维护，基于 ML 简化开发分支（simplified-dev）构建，已为 **30 款佳能相机**编译了可用的固件包。

### ✨ 魔灯能做什么？

魔灯为你的佳能相机添加了大量专业级功能，涵盖摄影和摄像两大领域：

#### 摄影功能
- **HDR 拍摄**：自动包围曝光，合成高动态范围照片
- **间隔拍摄（延时摄影）**：可配置间隔时间、拍摄张数、淡入淡出
- **运动检测**：基于画面变化触发快门
- **静音拍摄**：使用电子快门实现无声拍摄
- **曝光对齐（ETTR）**：向右曝光技术，最大化动态范围
- **焦距合成（Focus Stacking）**：自动改变焦点拍摄多张照片用于景深合成
- **焦点切换（Rack Focus）**：在两个焦点之间平滑过渡
- **多重曝光**：在单张照片上叠加多次曝光
- **闪光灯控制**：外接闪光灯的高级控制

#### 摄像功能
- **手动音频控制**：增益调节、风声滤波、实时波形监看
- **码率控制**：可调节 H.264 编码码率（CBR/VBR）
- **时间码**：SMPTE 时间码显示与同步
- **斑马纹**：过曝/欠曝区域高亮提示
- **假色**：用颜色映射亮度级别，专业曝光监看
- **直方图与矢量示波器**：实时画面分析
- **峰值对焦**：高亮显示合焦区域
- **平滑曝光过渡**：录像时平滑改变曝光参数
- **裁切模式**：3x/5x 数字变焦用于更精确的对焦

#### 显示与辅助
- **实时取景增强**：亮度、对比度、饱和度调节
- **网格线与安全框**：构图辅助线
- **电子水平仪**：双轴水平指示
- **自定义信息显示**：在屏幕上显示自定义参数
- **截图功能**：保存实时取景画面

#### 高级功能
- **原始视频（RAW Video）**：录制 14bit RAW 视频流
- **自定义菜单**：可编程的脚本菜单
- **Lua 脚本支持**：通过 Lua 扩展功能
- **模块系统**：可加载第三方模块扩展功能
- **固件调试工具**：寄存器查看、内存监控、任务管理等

### 📷 支持的机型

本项目已成功为以下 **30 款相机**编译了固件包：

| 机型 | 固件版本 | 类型 | 架构 |
|------|---------|------|------|
| **EOS 5D Mark II** | 2.1.2 | 全画幅单反 | ARMv5 |
| **EOS 5D Mark III** | 1.1.3 / 1.2.3 | 全画幅单反 | ARMv5 |
| **EOS 5D Mark IV** | 1.3.3 | 全画幅单反 | ARMv7 |
| **EOS 6D** | 1.1.6 | 全画幅单反 | ARMv5 |
| **EOS 6D Mark II** | 1.1.1 | 全画幅单反 | ARMv7 |
| **EOS 7D Mark II** | 1.1.2 | APS-C 单反 | ARMv5 |
| **EOS 40D** | 1.0.9 | APS-C 单反 | ARMv5 |
| **EOS 50D** | 1.0.9 | APS-C 单反 | ARMv5 |
| **EOS 60D** | 1.1.1 | APS-C 单反 | ARMv5 |
| **EOS 70D** | 1.1.2 | APS-C 单反 | ARMv5 |
| **EOS 77D** | 1.1.0 | APS-C 单反 | ARMv7 |
| **EOS 80D** | 1.0.3 | APS-C 单反 | ARMv7 |
| **EOS 450D** | 1.1.1 | APS-C 单反 | ARMv5 |
| **EOS 500D** | 1.1.1 | APS-C 单反 | ARMv5 |
| **EOS 550D** | 1.0.9 | APS-C 单反 | ARMv5 |
| **EOS 600D** | 1.0.2 | APS-C 单反 | ARMv5 |
| **EOS 650D** | 1.0.4 | APS-C 单反 | ARMv5 |
| **EOS 700D** | 1.1.5 | APS-C 单反 | ARMv5 |
| **EOS 750D** | 1.1.0 | APS-C 单反 | ARMv7 |
| **EOS 850D** | 1.0.0 | APS-C 单反 | ARMv7 |
| **EOS 100D** | 1.0.1 | APS-C 单反 | ARMv5 |
| **EOS 200D** | 1.0.1 | APS-C 单反 | ARMv7 |
| **EOS 1100D** | 1.0.5 | APS-C 单反 | ARMv5 |
| **EOS M** | 2.0.2 | 无反相机 | ARMv5 |
| **EOS M50** | 1.1.0 | 无反相机 | ARMv7 |
| **EOS M6 Mark II** | 1.1.1 | 无反相机 | ARMv7 |
| **EOS R** | 1.8.0 | 全画幅无反 | ARMv7 |
| **EOS R5** | 1.5.2 | 全画幅无反 | ARMv7 |
| **EOS RP** | 1.6.0 | 全画幅无反 | ARMv7 |
| **PowerShot SX70 HS** | 1.1.1 | 长焦相机 | ARMv7 |
| **PowerShot SX740 HS** | 1.0.2 | 长焦相机 | ARMv7 |

> ⚠️ **注意**：并非所有功能在所有机型上都可用。较新的机型（DIGIC 6/7/8）功能可能受限。

### 🔧 与原版的区别

| 特性 | 原版 Magic Lantern | 本汉化版 |
|------|-------------------|---------|
| **界面语言** | 英文 | 简体中文（菜单、选项、帮助文本） |
| **CJK 字体引擎** | 无 | 新增 `cjk_font.c`，支持 UTF-8 中日韩文字渲染 |
| **字体文件** | 仅 RBF 拉丁字体 | 新增 CJK 位图字体（12/23/28/32px，933 字形） |
| **模块描述** | 英文 | 已翻译 40 个模块的摘要和简述 |
| **构建用户** | 系统默认 | "Chase Chan" |
| **支持的机型** | 需逐个配置编译 | 已批量编译 30 款机型 |
| **源码** | 完整开发版 | 基于 simplified-dev 简化分支 |

**汉化范围**：
- 菜单名称、子菜单项、选项文本
- 帮助说明文本（`.help` / `.help2` 字段）
- 模块状态信息、模块描述
- 斑马纹、直方图等显示文本
- 错误提示、确认对话框文本

> **注意**：顶层菜单名称（Audio、Expo、Modules 等）保留英文，因为它们是 `menu.c` 中的内部查找键，翻译会导致菜单系统失效。

### 📦 安装到相机

#### 前提条件
- 一张 **FAT32 格式**的 SD 卡（≤32GB 或已格式化为 FAT32 的大容量卡）
- 相机固件版本必须与 ML 版本匹配

#### 安装步骤

1. **下载固件包**
   - 前往 [Releases 页面](https://github.com/ChaseChanCN/magiclantern/releases)
   - 下载对应你相机型号的 `magiclantern-XXXX.XXX.zip`

2. **解压到 SD 卡**
   ```
   将 zip 内容解压到 SD 卡根目录
   SD 卡根目录应包含:
     ├── ML/
     │   ├── fonts/
     │   ├── modules/
     │   ├── scripts/
     │   └── ...
     ├── autoexec.bin
     └── ML-SETUP.FIR
   ```

3. **首次安装 — 启用 bootflag**
   - 将 SD 卡插入相机
   - 开机，进入佳能菜单
   - 选择「固件版本」（Firmware Update）
   - 确认更新（实际上是安装 ML 的引导标记）
   - 相机重启后 ML 自动加载

4. **验证安装**
   - 相机开机时屏幕上会显示 ML 加载信息
   - 按 **MENU** 键或 **INFO** 键进入 ML 菜单
   - 按 **Q** 键快速切换 ML 显示

5. **卸载 ML**
   - 在佳能菜单中选择「固件版本」→ 更新 → 确认
   - 或格式化 SD 卡（会删除所有数据）

> ⚠️ **风险提示**：安装 Magic Lantern 可能导致相机保修失效。请自行承担风险。详细风险说明请参考 [magiclantern.fm](https://magiclantern.fm/)。

### 🛠️ 自行编译

#### 环境要求
- **操作系统**：Windows 10/11（推荐使用 Git Bash）
- **Python**：3.8+（注意：Windows Store 的 Python 不行，需安装真正的 Python）
- **ARM 工具链**：arm-none-eabi-gcc 15.x（xpack 版本）
- **Git**：任意版本
- **无需管理员权限**

#### 编译步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/ChaseChanCN/magiclantern.git
   cd magiclantern
   ```

2. **安装 ARM 工具链**（如果尚未安装）
   ```bash
   # 工具链会自动安装到 .build-deps/xpacks/
   # 首次编译时 Makefile 会自动下载
   ```

3. **设置环境变量**
   ```bash
   BIN="/path/to/magiclantern/.build-deps/xpacks/.bin"
   export PATH="$BIN:$PATH"
   ```

4. **编译指定机型**
   ```bash
   cd platform/70D.112  # 以 70D 为例
   make ARM_BINPATH="$BIN" -j4
   ```

5. **编译结果**
   ```
   platform/70D.112/build/
   ├── autoexec.bin      # ML 主程序
   ├── magiclantern.zip  # 完整安装包
   └── ML/
       └── ...           # SD 卡文件结构
   ```

6. **批量编译所有机型**
   ```bash
   # 参考项目根目录的 build_all.sh
   bash build_all.sh
   ```

#### 重新生成 CJK 字体

如果修改了翻译文本并引入了新的中文字符，需要重新生成字体：

```bash
cd localization

# 1. 提取所有源码中的 CJK 字符
py -3 extract_cjk_chars.py

# 2. 重新生成 4 种字号
for size in 12 23 28 32; do
  py -3 cjk_font_gen.py --chars all_chars.txt --size $size --out cjk${size}.crbf
  cp cjk${size}.crbf ../data/fonts/cjk${size}.rbf
done

# 3. 重新编译
cd ../platform/70D.112
make ARM_BINPATH="$BIN" -j4
```

### 📝 项目结构

```
magiclantern/
├── src/                    # ML 核心源码
│   ├── cjk_font.c/.h      # CJK 字体引擎（新增）
│   ├── rbf_font.c          # RBF 字体引擎（已补丁）
│   ├── menu.c              # 菜单系统
│   ├── shoot.c             # 拍摄功能
│   ├── focus.c             # 对焦功能
│   └── ...
├── modules/                # 可加载模块
├── platform/               # 各机型平台代码
│   ├── 70D.112/            # EOS 70D v1.1.2
│   ├── 5D3.113/            # EOS 5D Mark III v1.1.3
│   └── ...
├── data/fonts/             # 字体文件
│   ├── cjk12.rbf           # CJK 12px 字体
│   ├── cjk23.rbf           # CJK 23px 字体
│   ├── cjk28.rbf           # CJK 28px 字体
│   └── cjk32.rbf           # CJK 32px 字体
├── localization/           # 汉化工具与脚本
│   ├── cjk_font_gen.py     # CJK 字体生成器
│   ├── extract_cjk_chars.py # 字符提取脚本
│   ├── apply_zh_full.py    # 翻译应用脚本
│   └── ...
└── build_all.sh            # 批量编译脚本
```

### 🙏 致谢

- [Magic Lantern 团队](https://magiclantern.fm/) — 原始项目开发
- 所有 ML 社区贡献者
- 简化开发分支（simplified-dev）的维护者

### ⚖️ 许可证

GPL v2 或更高版本。详见 [LICENSE](LICENSE)。

### 🔗 相关链接

- 官方网站：[https://magiclantern.fm/](https://magiclantern.fm/)
- 官方论坛：[https://magiclantern.fm/forum/](https://magiclantern.fm/forum/)
- 本项目 GitHub：[https://github.com/ChaseChanCN/magiclantern](https://github.com/ChaseChanCN/magiclantern)

---

## English Version

Magic Lantern (ML) is an open-source software enhancement platform that provides additional functionality for Canon digital cameras. It is released under the GPL license and runs independently alongside Canon's official firmware — **it does not replace or modify the original firmware**.

This project is a **Simplified Chinese localization** of Magic Lantern, maintained by [Chase Chan](https://github.com/ChaseChanCN), based on the ML simplified-dev branch. Firmware packages have been compiled for **30 Canon cameras**.

### ✨ What Can Magic Lantern Do?

ML adds professional-grade features covering both photography and videography:

#### Photography
- **HDR Shooting**: Auto exposure bracketing for high dynamic range composites
- **Intervalometer (Timelapse)**: Configurable interval, shot count, ramping
- **Motion Detection**: Trigger shutter based on scene changes
- **Silent Shooting**: Electronic shutter for noiseless capture
- **ETTR (Expose To The Right)**: Maximize dynamic range
- **Focus Stacking**: Auto-focus bracketing for depth-of-field composites
- **Rack Focus**: Smooth focus transitions between two points
- **Multiple Exposures**: Overlay multiple exposures on a single frame
- **Flash Control**: Advanced external flash control

#### Videography
- **Manual Audio Control**: Gain adjustment, wind filter, real-time waveform
- **Bitrate Control**: Adjustable H.264 encoding bitrate (CBR/VBR)
- **Timecode**: SMPTE timecode display and sync
- **Zebras**: Over/underexposure area highlighting
- **False Color**: Color-mapped luminance for professional exposure monitoring
- **Histogram & Vectorscope**: Real-time scene analysis
- **Focus Peaking**: Highlight in-focus areas
- **Smooth Exposure Transitions**: Smoothly change exposure while recording
- **Crop Mode**: 3x/5x digital zoom for precise focusing

#### Display & Assistance
- **LiveView Enhancement**: Brightness, contrast, saturation adjustment
- **Grid Lines & Safe Frames**: Composition guides
- **Electronic Level**: Dual-axis level indicator
- **Custom Info Display**: Show custom parameters on screen
- **Screenshot**: Save LiveView frame

#### Advanced
- **RAW Video**: Record 14bit RAW video stream
- **Custom Menu**: Programmable script menu
- **Lua Scripting**: Extend functionality via Lua
- **Module System**: Load third-party modules
- **Debug Tools**: Register viewer, memory monitor, task manager

### 📷 Supported Cameras

Firmware packages have been successfully compiled for **30 cameras**:

| Camera | Firmware | Type | Architecture |
|--------|----------|------|-------------|
| **EOS 5D Mark II** | 2.1.2 | Full-frame DSLR | ARMv5 |
| **EOS 5D Mark III** | 1.1.3 / 1.2.3 | Full-frame DSLR | ARMv5 |
| **EOS 5D Mark IV** | 1.3.3 | Full-frame DSLR | ARMv7 |
| **EOS 6D** | 1.1.6 | Full-frame DSLR | ARMv5 |
| **EOS 6D Mark II** | 1.1.1 | Full-frame DSLR | ARMv7 |
| **EOS 7D Mark II** | 1.1.2 | APS-C DSLR | ARMv5 |
| **EOS 40D** | 1.0.9 | APS-C DSLR | ARMv5 |
| **EOS 50D** | 1.0.9 | APS-C DSLR | ARMv5 |
| **EOS 60D** | 1.1.1 | APS-C DSLR | ARMv5 |
| **EOS 70D** | 1.1.2 | APS-C DSLR | ARMv5 |
| **EOS 77D** | 1.1.0 | APS-C DSLR | ARMv7 |
| **EOS 80D** | 1.0.3 | APS-C DSLR | ARMv7 |
| **EOS 450D** | 1.1.1 | APS-C DSLR | ARMv5 |
| **EOS 500D** | 1.1.1 | APS-C DSLR | ARMv5 |
| **EOS 550D** | 1.0.9 | APS-C DSLR | ARMv5 |
| **EOS 600D** | 1.0.2 | APS-C DSLR | ARMv5 |
| **EOS 650D** | 1.0.4 | APS-C DSLR | ARMv5 |
| **EOS 700D** | 1.1.5 | APS-C DSLR | ARMv5 |
| **EOS 750D** | 1.1.0 | APS-C DSLR | ARMv7 |
| **EOS 850D** | 1.0.0 | APS-C DSLR | ARMv7 |
| **EOS 100D** | 1.0.1 | APS-C DSLR | ARMv5 |
| **EOS 200D** | 1.0.1 | APS-C DSLR | ARMv7 |
| **EOS 1100D** | 1.0.5 | APS-C DSLR | ARMv5 |
| **EOS M** | 2.0.2 | Mirrorless | ARMv5 |
| **EOS M50** | 1.1.0 | Mirrorless | ARMv7 |
| **EOS M6 Mark II** | 1.1.1 | Mirrorless | ARMv7 |
| **EOS R** | 1.8.0 | Full-frame mirrorless | ARMv7 |
| **EOS R5** | 1.5.2 | Full-frame mirrorless | ARMv7 |
| **EOS RP** | 1.6.0 | Full-frame mirrorless | ARMv7 |
| **PowerShot SX70 HS** | 1.1.1 | Superzoom | ARMv7 |
| **PowerShot SX740 HS** | 1.0.2 | Superzoom | ARMv7 |

> ⚠️ **Note**: Not all features are available on all cameras. Newer cameras (DIGIC 6/7/8) may have limited functionality.

### 🔧 Differences from Original ML

| Feature | Original Magic Lantern | This Localization |
|---------|----------------------|-------------------|
| **UI Language** | English | Simplified Chinese (menus, choices, help) |
| **CJK Font Engine** | None | Added `cjk_font.c` with UTF-8 CJK rendering |
| **Font Files** | RBF Latin only | Added CJK bitmap fonts (12/23/28/32px, 933 glyphs) |
| **Module Descriptions** | English | 40 module summaries translated |
| **Build User** | System default | "Chase Chan" |
| **Supported Cameras** | Per-camera setup | 30 cameras pre-compiled |
| **Source** | Full dev branch | Based on simplified-dev branch |

**Localization Scope**:
- Menu names, sub-menu items, choice text
- Help text (`.help` / `.help2` fields)
- Module status info and descriptions
- Zebra, histogram display text
- Error messages, confirmation dialogs

> **Note**: Top-level menu names (Audio, Expo, Modules, etc.) remain in English as they are internal lookup keys in `menu.c` — translating them breaks the menu system.

### 📦 Installation

#### Prerequisites
- A **FAT32-formatted** SD card (≤32GB, or larger card formatted as FAT32)
- Camera firmware version must match the ML version

#### Steps

1. **Download firmware package**
   - Go to [Releases page](https://github.com/ChaseChanCN/magiclantern/releases)
   - Download `magiclantern-XXXX.XXX.zip` for your camera model

2. **Extract to SD card**
   ```
   Extract zip contents to SD card root:
   SD card root:
     ├── ML/
     │   ├── fonts/
     │   ├── modules/
     │   ├── scripts/
     │   └── ...
     ├── autoexec.bin
     └── ML-SETUP.FIR
   ```

3. **First install — Enable bootflag**
   - Insert SD card into camera
   - Power on, enter Canon menu
   - Select "Firmware Update"
   - Confirm update (this installs ML's boot flag)
   - Camera restarts with ML loaded

4. **Verify installation**
   - ML loading info appears at startup
   - Press **MENU** or **INFO** to access ML menu
   - Press **Q** to toggle ML display

5. **Uninstall ML**
   - Canon menu → "Firmware Update" → Update → Confirm
   - Or format SD card (erases all data)

> ⚠️ **Disclaimer**: Installing Magic Lantern may void your camera warranty. Proceed at your own risk. See [magiclantern.fm](https://magiclantern.fm/) for details.

### 🛠️ Building from Source

#### Requirements
- **OS**: Windows 10/11 (Git Bash recommended)
- **Python**: 3.8+ (real Python, not Windows Store stub)
- **ARM Toolchain**: arm-none-eabi-gcc 15.x (xpack)
- **Git**: any version
- **No admin rights needed**

#### Steps

1. **Clone repository**
   ```bash
   git clone https://github.com/ChaseChanCN/magiclantern.git
   cd magiclantern
   ```

2. **Install ARM toolchain** (if not already installed)
   ```bash
   # Toolchain auto-installs to .build-deps/xpacks/
   # Makefile downloads it on first build
   ```

3. **Set environment**
   ```bash
   BIN="/path/to/magiclantern/.build-deps/xpacks/.bin"
   export PATH="$BIN:$PATH"
   ```

4. **Build a specific camera**
   ```bash
   cd platform/70D.112  # e.g., 70D
   make ARM_BINPATH="$BIN" -j4
   ```

5. **Build output**
   ```
   platform/70D.112/build/
   ├── autoexec.bin      # ML main program
   ├── magiclantern.zip  # Complete install package
   └── ML/
       └── ...           # SD card file structure
   ```

6. **Build all cameras**
   ```bash
   bash build_all.sh
   ```

#### Regenerating CJK Fonts

If you modify translations and introduce new Chinese characters, regenerate fonts:

```bash
cd localization

# 1. Extract all CJK characters from source
py -3 extract_cjk_chars.py

# 2. Regenerate all 4 sizes
for size in 12 23 28 32; do
  py -3 cjk_font_gen.py --chars all_chars.txt --size $size --out cjk${size}.crbf
  cp cjk${size}.crbf ../data/fonts/cjk${size}.rbf
done

# 3. Rebuild
cd ../platform/70D.112
make ARM_BINPATH="$BIN" -j4
```

### 📝 Project Structure

```
magiclantern/
├── src/                    # ML core source
│   ├── cjk_font.c/.h      # CJK font engine (new)
│   ├── rbf_font.c          # RBF font engine (patched)
│   ├── menu.c              # Menu system
│   ├── shoot.c             # Shooting features
│   ├── focus.c             # Focus features
│   └── ...
├── modules/                # Loadable modules
├── platform/               # Per-camera platform code
│   ├── 70D.112/            # EOS 70D v1.1.2
│   ├── 5D3.113/            # EOS 5D Mark III v1.1.3
│   └── ...
├── data/fonts/             # Font files
│   ├── cjk12.rbf           # CJK 12px font
│   ├── cjk23.rbf           # CJK 23px font
│   ├── cjk28.rbf           # CJK 28px font
│   └── cjk32.rbf           # CJK 32px font
├── localization/           # Localization tools
│   ├── cjk_font_gen.py     # CJK font generator
│   ├── extract_cjk_chars.py # Character extraction
│   ├── apply_zh_full.py    # Translation application
│   └── ...
└── build_all.sh            # Batch build script
```

### 🙏 Credits

- [Magic Lantern Team](https://magiclantern.fm/) — Original project
- All ML community contributors
- simplified-dev branch maintainers

### ⚖️ License

GPL v2 or later. See [LICENSE](LICENSE).

### 🔗 Links

- Official website: [https://magiclantern.fm/](https://magiclantern.fm/)
- Official forum: [https://magiclantern.fm/forum/](https://magiclantern.fm/forum/)
- This project: [https://github.com/ChaseChanCN/magiclantern](https://github.com/ChaseChanCN/magiclantern)
