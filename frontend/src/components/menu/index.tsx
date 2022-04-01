import React from 'react'
import { Link } from 'react-router-dom'
import classnames from 'classnames/bind'
import styles from './menu.module.scss'
const cx = classnames.bind(styles)

export default function Menu() {
    return (
        <div className={cx('main')}>
            <ul className={cx('list')}>
                <Link to="/tier" className={cx('link')}>
                    <li className={cx('li')}>레벨별 미해결 문제</li>
                </Link>
                <Link to="/tag" className={cx('link')}>
                    <li className={cx('li')}>태그별 미해결 문제</li>
                </Link>
            </ul>
        </div>
    )
}
