import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/team/')({
  component: () => <div>Team listing page</div>,
})
