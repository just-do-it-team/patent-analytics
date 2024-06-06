import { Typography } from 'antd';
import { StopOutlined } from '@ant-design/icons';
import { memo } from 'react';
import { useAppSelector } from '@/app/providers/store-provider/config/hooks';
import classes from './fetchError.module.scss';

export const FetchError = memo(() => {
    const { searchString, searchResult } = useAppSelector((state) => state.category);
    return (
        <div className={classes.container}>
            <StopOutlined className={classes.icon} />
            <Typography className={classes.message}>
                {searchString && !searchResult ? 'Нет данных' : 'Не удалось загрузить данные'}
            </Typography>
        </div>
    );
});
