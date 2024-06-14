import { memo } from "react"
import {
  useAppDispatch,
  useAppSelector,
} from "@/app/providers/store-provider/config/hooks"
import { closeModal } from "@/entities/import/model/slice/importSlice"
import { ModalComponent } from "@/shared/ui/modal"
import { FilterHistoryForm } from "@/features/filter-history-form"

export const FilterHistoryModal = memo(() => {
  const dispatch = useAppDispatch()
  const { isOpenModal } = useAppSelector(state => state.import)

  const hideModal = () => {
    dispatch(closeModal())
  }

  return (
    <ModalComponent open={isOpenModal} onCancel={hideModal} destroyOnClose>
      <FilterHistoryForm />
    </ModalComponent>
  )
})
