### Build 32-bit

```
cargo build --target=i686-pc-windows-msvc --release
```

Output file: `.\target\i686-pc-windows-msvc\release\rhttp.dll`


### Build 64-bit

```
cargo build --target=x86_64-pc-windows-msvc --release
```

Output file: `.\target\x86_64-pc-windows-msvc\release\rhttp.dll`

### Test via python 3

```
> python3 .\test.py --dll .\target\x86_64-pc-windows-msvc\release\rhttp.dll
16
2.25
6.25
5
Szia, Apu!
aaaaa
ő na na na na na Batman! ő
(True, 'YW55IGNhcm5hbCBwbGVhc3VyZS4=', 'any carnal pleasure.')
(True, '7b6f7690ae2a5ecdf66b3db2adf91340a680da1ab82561796b8504db942476967369814aa35050dd86838848c1ba703450f2f5e21b0a8e4cff690b855ae5bd8c', '7b6f7690ae2a5ecdf66b3db2adf91340a680da1ab82561796b8504db942476967369814aa35050dd86838848c1ba703450f2f5e21b0a8e4cff690b855ae5bd8c')
(True, 'ef846feafed891792553756277b48e90784eca281f683920551f36b359833b10aab4897765050e398232e3f213fe49c7c50271f339d4797c25dc58c3d7f33f81', 'ef846feafed891792553756277b48e90784eca281f683920551f36b359833b10aab4897765050e398232e3f213fe49c7c50271f339d4797c25dc58c3d7f33f81')
```

### VFP notes

```
DECLARE sha3_512_encode "rhttp.dll" @STRING, @STRING

testString = "TestVFP"
sha512_encode(0, @testString )

```