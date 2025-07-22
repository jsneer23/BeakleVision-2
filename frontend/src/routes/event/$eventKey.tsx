import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/event/$eventKey')({
  component: () => <div>Hello /event/$eventKey!</div>
})
