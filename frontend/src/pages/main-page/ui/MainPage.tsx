import { classNames } from "@/shared/lib/classNames/classNames"
import classes from "./mainPage.module.scss"
import { Block } from "@/shared/ui/block/Block"
import { Button, Flex } from "antd"

interface MainPageProps {
  className?: string
}

const MainPage = ({ className }: MainPageProps) => (
  <div className={classNames(classes.MainPage, {}, [className])}>
    <Block>
      <Flex gap="small" wrap="wrap">
        <Button type="primary" className={classes.primary}>
          Primary Button
        </Button>
        <Button>Default Button</Button>
        <Button type="dashed">Dashed Button</Button>
        <Button type="text">Text Button</Button>
        <Button type="link">Link Button</Button>
      </Flex>
    </Block>
  </div>
)

export default MainPage
