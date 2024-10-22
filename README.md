# fuse-blog
mountable, virtual filesystem for reading and writing my blog.


### Prerequisites

- **Python 3.11**
- **uv** package manager
- **FUSE** library

### Install Dependencies

1. **Clone the Repository**

   ```
   git clone https://github.com/gashon/fuse-blog.git
   cd fuse-blog
   ```

2. **Set Up Virtual Environment** (Optional but Recommended)

   ```
   uv venv --python=3.11
   source venv/bin/activate
   ```

3. **Install Python Packages**

   ```
   uv pip install -r requirements.txt
   ```

4. **Install FUSE**

   - **Ubuntu/Debian**

     ```
     sudo apt-get install fuse
     ```

   - **macOS**

     ```
     brew install macfuse
     ```

## Usage

### Mount the Filesystem

```
python blog_fuse.py <mountpoint>
```

### Examples

**List Files**

```
ls -l <mountpoint>
```

**Read a File**

```
cat <mountpoint>/2024-01-01_12-00-00_<post_id>.txt
```
