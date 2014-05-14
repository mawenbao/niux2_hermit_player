# -*- coding: UTF-8 -*-
"""
Hermit player(http://mufeng.me/hermit-for-wordpress.html) plugin for niu-x2-sidebar theme.

This plugin replaces the [hermit id=[0-9]+ loop auto] with hermit player html structure.
"""

from pelican import signals
import re
import logging

logger = logging.getLogger(__name__)
_hermit_begin_code = '[hermit'
_hermit_end_code = ']'
_hermit_loop = 'loop'
_hermit_auto = 'auto'
_hermit_id = 'id'
_hermit_source = '''
<div class="hermit" songs="collect#:{id}" loop="{loop}" auto="{auto}">
    <div class="hermit-box">
        <div class="hermit-controls">
            <div class="hermit-button">
            </div>
            <div class="hermit-detail">
                单击鼠标左键播放或暂停
            </div>
            <div class="hermit-duration">
            </div>
            <div class="hermit-listbutton">
            </div>
        </div>
        <div class="hermit-prosess">
            <div class="hermit-loaded">
            </div>
            <div class="hermit-prosess-bar">
                <div class="hermit-prosess-after">
                </div>
            </div>
        </div>
    </div>
    <div class="hermit-list">
    </div>
</div>
'''

def parse_hermit(instance):
    if instance._content is None:
        return
    start = 0
    content = instance._content
    contentParts = []
    while start < len(content):
        hermitBeginPos = content[start:].find(_hermit_begin_code)
        if -1 == hermitBeginPos:
            break
        hermitEndPos = content[hermitBeginPos:].find(_hermit_end_code)
        if -1 == hermitEndPos:
            logger.error('no end bracket found for [hermit in source %s:%d', instance.source_path, hermitBeginPos)
            return
        hermitEndPos += hermitBeginPos
        if content[start : hermitBeginPos]:
            contentParts.append(content[start : hermitBeginPos])
        hermitCode = content[hermitBeginPos + len(_hermit_begin_code) : hermitEndPos]
        hermitCtrl = hermitCode.split()
        hermitLoop = '0'
        hermitAuto = '0'
        if _hermit_loop in hermitCtrl:
            hermitCtrl.remove(_hermit_loop)
            hermitLoop = '1'
        if _hermit_auto in hermitCtrl:
            hermitCtrl.remove(_hermit_auto)
            hermitAuto = '1'
        if not hermitCtrl or not hermitCtrl[0].startswith(_hermit_id):
            logger.error('no xiami album id in hermit code, source %s:%d', instance.source_path, hermitBeginPos)
            return
        try:
            hermitAlbumId = int(hermitCtrl[0].split('=')[1])
        except Exception as e:
            logger.error('failed to extrace xiami album id from hermit code: %s: source %s:%d', e, instance.source_path, hermitBeginPos)
            return
        contentParts.append(_hermit_source.format(id=hermitAlbumId, loop=hermitLoop, auto=hermitAuto))
        start = hermitEndPos + 1 
    if contentParts:
        contentParts.append(content[start:])
        instance._content = ''.join(contentParts)

def register():
    signals.content_object_init.connect(parse_hermit)

