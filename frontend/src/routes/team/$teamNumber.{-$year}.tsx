import { createFileRoute } from "@tanstack/react-router"
import { Box, Heading, Text } from "@chakra-ui/react"

import { type Team, TeamService } from "@/client"

export const Route = createFileRoute('/team/$teamNumber/{-$year}')({
  component: TeamPage,
  loader: async ({ params }) => {
    const teamInt: number = parseInt(params.teamNumber, 10)
    const team: Team = await TeamService.getTeamByNumber({ number: teamInt })
    return { Team: team }
  },
})

// Define the component that will be rendered for this route
function TeamPage() {

  const { year } = Route.useParams()
  const { Team: team } = Route.useLoaderData()
  return (
    <Box p={8}>
      <Heading mb={4}>Team {team.number} - {team.nickname}</Heading>
      <Text mb={4}> {team.city}, {team.state_prov}, {team.country} </Text>
      <Text mb={4}> Rookie year: {team.rookie_year} </Text>
    </Box>
  )
}