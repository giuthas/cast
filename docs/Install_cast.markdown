# Install CAST

There's two main methods: Use either pip or uv. 

NOTE: Which ever you use, please note that CAST's Python package name is
computer-assisted-segmentation-tools. When installing from PyPi (with pip or uv
or some other tool) you will need to use this long name. There is a different
package on PyPi with the name cast and installing that will not get you the
right package.

## Using pip

This will work as soon as CAST is on pypi. 

## Using uv

There are other more programming oriented ways of running a package like CAST
with uv, but the following assumes the aim is to have a ordinary command line
command installed for ease of use.

Also of note is that the current way is just a hack as it is. See
[below](#when-pypi-is-available).

1. Get [uv](https://docs.astral.sh/uv/getting-started/installation/)
    - If you have no specific preference for install method, use the first system
      appropriate one from the linked page.
2. Get the CAST sources. Here are alternative ways of doing that:
   - Download and unpack them from
      [GitHub](https://github.com/giuthas-speech-research-tools/cast/releases), or
   - clone the repository with ´git clone
      https://github.com/giuthas-speech-research-tools/cast/´, 
   - or clone your own fork if you have forked CAST.
3. In the (unpacked) source directory run 'uv tool install .' This will install two
   command line commands: `cast` and `computer-assisted-segmentation-tools`. The
   name of the installed package is computer-assisted-segmentation-tools.
4. See `cast --help` for help and `cast [command] --help` for more specific
   instructions and the documentation for even more.

If you need to upgrade CAST, first obtain updated sources (or edit them
yourself), then run `uv tool upgrade computer-assisted-segmentation-tools
--reinstall` in the same directory. The `--reinstall` will be needed if the
versionnumber or dependencies didn't update -- a usual case for needing this is
making some changes in the code and wanting to test them out.

### When PyPi is available

Once CAST is on PyPi, you can skip from step 1 to just running `uv tool install
computer-assisted-segmentation-tools`.  Upgrading to latest PyPi version will
also simplify to just running `uv tool upgrade
computer-assisted-segmentation-tools`.

If you do a PyPi install and want to test local code do it with `uv run cast`.
If you only require an installation to test local code and want to use the short
`cast` instead of `uv run cast`, use the [above](Install_cast.markdown#using-uv)
instructions.
