import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/event/')({
  component: () => <div>Hello /event/!</div>
})
