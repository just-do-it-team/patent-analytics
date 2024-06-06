import { ReactNode } from 'react';
import { Provider } from 'react-redux';
import store from '@/app/providers/store-provider/config/store';

interface StoreProviderProps {
    children?: ReactNode;
}

export const StoreProvider = (props: StoreProviderProps) => {
    const {
        children,
    } = props;

    return (
        <Provider store={store}>
            {children}
        </Provider>
    );
};
