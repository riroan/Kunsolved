import React, { useState } from 'react'
import classnames from 'classnames/bind'
import styles from './issue.module.scss'
import URL from '../_config/config'
const cx = classnames.bind(styles)

export default function Issue() {
    const [text, setText] = useState<string>('')
    const onChange = (e: React.FormEvent<HTMLInputElement>) => {
        setText(e.currentTarget.value)
    }
    const submit = () => {
        var url = `${URL}/v1/issue`
        const body = { text: text }
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        })
            .then(res => res.json())
            .then(res => {
                alert('전송에 성공했습니다.')
            })
            .catch(err => {
                alert('전송에 실패했습니다.')
            })
    }
    return (
        <div className={cx('box')}>
            <div className={cx('title')}>기능요청</div>
            <div className={cx('desc')}>원하는 기능을 알려주세요.</div>
            <div className={cx('desc')}>
                <a href={'https://github.com/riroan/SchoolJoon/blob/main/TODO.md'} target="_blank" rel="noopener noreferrer">현재 추가 계획이 있는 기능</a>
            </div>
            <input type="text" className={cx('input')} maxLength={200} onChange={onChange} />
            <button className={cx('button')} disabled={text.length === 0} onClick={submit}>
                보내기
            </button>
        </div>
    )
}
