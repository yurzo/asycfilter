#!/usr/bin/env python3
import asyncio
import socket
import subprocess
import sys

# import click

async def handle_stream(stream, name):
    # with open(stream, 'r') as hndl:
    # breakpoint()
    while True:
        # await asyncio.sleep(0)
        # data = await stream.readuntil()
        data = await stream.readline()
        if data:
            print('{}: {}'.format(name, data.decode().strip()), file=sys.stdout)
            sys.stdout.flush()
        await asyncio.sleep(0)



async def get_stdout_line(proc):
    while True:
        data = await proc.stdout.readline()
        if data:
            print('Out: {}'.format(data.decode().strip()))
        await asyncio.sleep(0)

async def get_stderr_line(proc):
    while True:
        data = await proc.stderr.readline()
        if data:
            print('Err: {}'.format(data.decode().strip()))
        await asyncio.sleep(0)

async def _asyncfilter(cmd):
    # Create the subprocess, redirect the standard output into a pipe

    #out_reader, out_writer = await asyncio.open_connection('127.0.0.1')
    #err_reader, err_writer = await asyncio.open_connection('127.0.0.1')

    # rsock, wsock = socket.socketpair()
    # out_reader, out_writer = await asyncio.open_connection(sock=rsock)
    #
    # rsock, wsock = socket.socketpair()
    # err_reader, err_writer = await asyncio.open_connection(sock=rsock)


    out_rsock, out_wsock = socket.socketpair()
    out_w = out_wsock.makefile('wb', buffering=0)
    # out_r = out_rsock.makefile('rb')
    out_reader, _ = await asyncio.open_connection(sock=out_rsock)

    err_rsock, err_wsock = socket.socketpair()
    err_w = err_wsock.makefile('wb', buffering=0)
    # err_r = err_rsock.makefile('rb')
    err_reader, _ = await asyncio.open_connection(sock=err_rsock)

    setattr(out_w, 'isatty', lambda: True)
    setattr(err_w, 'isatty', lambda: True)
    import os
    setattr(os, 'isatty', lambda x: True)


    proc = await asyncio.create_subprocess_exec(
        *cmd,
        # stdin=None,
        # stdout=asyncio.subprocess.PIPE,
        # stdout=out_writer,
        stdout=out_w,
        # stderr=asyncio.subprocess.PIPE,
        # stderr=err_writer,
        stderr=err_w,

        close_fds=True,
        # stderr=err,
        bufsize=0,
        limit=0,
        # shell=True,
        #stdout=out_writer,
        #stderr=err_writer
        )

    loop = asyncio.get_event_loop()

    # t1 = loop.create_task(get_stdout_line(proc))
    # t2 = loop.create_task(get_stderr_line(proc))

    # t1 = loop.create_task(handle_stream(proc.stdout, 'Out'))
    # t1 = loop.create_task(handle_stream(reader, 'Out'))
    t1 = loop.create_task(handle_stream(out_reader, 'Out'))
    # t2 = loop.create_task(handle_stream(proc.stderr, 'Err'))
    t2 = loop.create_task(handle_stream(err_reader, 'Err'))

    # breakpoint()
    await proc.wait()

    t1.cancel()
    t2.cancel()

# @click.command()
# @click.argument('cmd', nargs=-1, type=str)
def asyncfilter(cmd):
    '''a filter for both your stdout and stderr without mesing them ups'''

    # print(cmd)

    if sys.platform == "win32":
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()

    loop.run_until_complete(_asyncfilter(cmd))
    loop.close()
    #coro = asyncio.create_subprocess_exec(*args, stdin=None, stdout=None, stderr=None, loop=None, limit=None, **kwds)¶


if __name__ == '__main__':
    # asyncfilter(sys.argv[1:])

    asyncfilter(sys.argv[1:])
